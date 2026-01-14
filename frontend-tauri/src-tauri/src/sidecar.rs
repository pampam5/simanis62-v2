//! Sidecar manager untuk Python FastAPI backend.
//!
//! Module ini menangani lifecycle sidecar:
//! - Spawn sidecar on startup
//! - Health check polling
//! - Graceful shutdown

use std::sync::Arc;
use std::time::Duration;
use tauri::async_runtime::Mutex;
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;
use log::{info, warn, error};

use crate::error::SidecarError;

/// Backend API configuration
const API_HOST: &str = "127.0.0.1";
const API_PORT: u16 = 8000;
const HEALTH_CHECK_TIMEOUT_SECS: u64 = 30;
const HEALTH_CHECK_INTERVAL_MS: u64 = 500;

/// Sidecar state yang di-share antar commands
pub struct SidecarState {
    pub child: Option<CommandChild>,
    pub is_ready: bool,
}

impl Default for SidecarState {
    fn default() -> Self {
        Self {
            child: None,
            is_ready: false,
        }
    }
}

/// Type alias untuk shared sidecar state
pub type SharedSidecarState = Arc<Mutex<SidecarState>>;

/// Spawn sidecar process
pub async fn spawn_sidecar(
    app: &tauri::AppHandle,
    state: SharedSidecarState,
) -> Result<(), SidecarError> {
    info!("Spawning Python FastAPI sidecar...");

    let shell = app.shell();

    // Spawn sidecar dengan tauri-plugin-shell
    let (mut rx, child) = shell
        .sidecar("bin/api/simanis62-api")
        .map_err(|e| SidecarError::SpawnFailed(e.to_string()))?
        .spawn()
        .map_err(|e| SidecarError::SpawnFailed(e.to_string()))?;

    // Store child process
    {
        let mut state_guard = state.lock().await;
        state_guard.child = Some(child);
    }

    // Spawn task untuk handle sidecar output
    let state_clone = state.clone();
    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(line) => {
                    let line_str = String::from_utf8_lossy(&line);
                    info!("[API] {}", line_str);
                }
                CommandEvent::Stderr(line) => {
                    let line_str = String::from_utf8_lossy(&line);
                    warn!("[API] {}", line_str);
                }
                CommandEvent::Terminated(payload) => {
                    error!(
                        "Sidecar terminated with code: {:?}, signal: {:?}",
                        payload.code, payload.signal
                    );
                    let mut state_guard = state_clone.lock().await;
                    state_guard.is_ready = false;
                    state_guard.child = None;
                }
                _ => {}
            }
        }
    });

    info!("Sidecar spawned, waiting for health check...");
    Ok(())
}

/// Check apakah backend sudah ready
pub async fn check_backend_health() -> Result<bool, SidecarError> {
    let url = format!("http://{}:{}/api/v1/health", API_HOST, API_PORT);

    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(2))
        .build()
        .map_err(|e| SidecarError::ConnectionFailed(e.to_string()))?;

    match client.get(&url).send().await {
        Ok(response) => Ok(response.status().is_success()),
        Err(_) => Ok(false),
    }
}

/// Wait sampai backend ready dengan polling
pub async fn wait_for_backend_ready(
    state: SharedSidecarState,
) -> Result<(), SidecarError> {
    info!("Waiting for backend to be ready...");

    let start = std::time::Instant::now();
    let timeout = Duration::from_secs(HEALTH_CHECK_TIMEOUT_SECS);

    loop {
        if start.elapsed() > timeout {
            return Err(SidecarError::HealthCheckTimeout(HEALTH_CHECK_TIMEOUT_SECS));
        }

        match check_backend_health().await {
            Ok(true) => {
                info!("Backend is ready!");
                let mut state_guard = state.lock().await;
                state_guard.is_ready = true;
                return Ok(());
            }
            Ok(false) => {
                // Backend belum ready, tunggu dan coba lagi
                tokio::time::sleep(Duration::from_millis(HEALTH_CHECK_INTERVAL_MS)).await;
            }
            Err(e) => {
                warn!("Health check error: {}", e);
                tokio::time::sleep(Duration::from_millis(HEALTH_CHECK_INTERVAL_MS)).await;
            }
        }
    }
}

/// Graceful shutdown sidecar
pub async fn shutdown_sidecar(state: SharedSidecarState) -> Result<(), SidecarError> {
    info!("Shutting down sidecar...");

    let mut state_guard = state.lock().await;

    if let Some(child) = state_guard.child.take() {
        // Kill the process
        if let Err(e) = child.kill() {
            warn!("Failed to kill sidecar: {}", e);
        }
    }

    state_guard.is_ready = false;
    info!("Sidecar shutdown complete");
    Ok(())
}
