using System.Net;
using System.Net.Http;
using Polly;
using Polly.Extensions.Http;
using Polly.Retry;
using Polly.CircuitBreaker;
using Polly.Timeout;
using Serilog;

namespace Simanis62.Services;

/// <summary>
/// Polly resilience policies untuk HTTP client.
/// Implements retry, circuit breaker, dan timeout patterns.
/// </summary>
public static class ResiliencePolicies
{
    private static readonly ILogger Logger = Log.ForContext(typeof(ResiliencePolicies));

    /// <summary>
    /// Get combined resilience policy (Retry + Circuit Breaker + Timeout).
    /// </summary>
    public static IAsyncPolicy<HttpResponseMessage> GetCombinedPolicy()
    {
        return Policy.WrapAsync(
            GetRetryPolicy(),
            GetCircuitBreakerPolicy(),
            GetTimeoutPolicy()
        );
    }

    /// <summary>
    /// Retry policy dengan exponential backoff.
    /// Retry 3x untuk transient HTTP errors (5xx, 408, network errors).
    /// </summary>
    public static AsyncRetryPolicy<HttpResponseMessage> GetRetryPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError() // 5xx, 408, HttpRequestException
            .OrResult(msg => msg.StatusCode == HttpStatusCode.TooManyRequests) // 429
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)), // 2, 4, 8 seconds
                onRetry: (outcome, timespan, retryAttempt, context) =>
                {
                    Logger.Warning(
                        "Retry {RetryAttempt} after {Delay}s due to {StatusCode}",
                        retryAttempt,
                        timespan.TotalSeconds,
                        outcome.Result?.StatusCode ?? HttpStatusCode.ServiceUnavailable);
                });
    }

    /// <summary>
    /// Circuit breaker policy.
    /// Opens circuit after 5 consecutive failures, stays open for 30 seconds.
    /// </summary>
    public static AsyncCircuitBreakerPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .CircuitBreakerAsync(
                handledEventsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30),
                onBreak: (outcome, breakDelay) =>
                {
                    Logger.Warning(
                        "Circuit breaker opened for {BreakDelay}s due to {StatusCode}",
                        breakDelay.TotalSeconds,
                        outcome.Result?.StatusCode ?? HttpStatusCode.ServiceUnavailable);
                },
                onReset: () =>
                {
                    Logger.Information("Circuit breaker reset - connection restored");
                },
                onHalfOpen: () =>
                {
                    Logger.Information("Circuit breaker half-open - testing connection");
                });
    }

    /// <summary>
    /// Timeout policy - 30 seconds per request.
    /// </summary>
    public static AsyncTimeoutPolicy<HttpResponseMessage> GetTimeoutPolicy()
    {
        return Policy.TimeoutAsync<HttpResponseMessage>(
            TimeSpan.FromSeconds(30),
            TimeoutStrategy.Optimistic,
            onTimeoutAsync: (context, timespan, task) =>
            {
                Logger.Warning("Request timed out after {Timeout}s", timespan.TotalSeconds);
                return Task.CompletedTask;
            });
    }

    /// <summary>
    /// Simple retry policy untuk non-HTTP operations.
    /// </summary>
    public static AsyncRetryPolicy GetSimpleRetryPolicy()
    {
        return Policy
            .Handle<HttpRequestException>()
            .Or<TaskCanceledException>()
            .Or<TimeoutException>()
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
                onRetry: (exception, timespan, retryAttempt, context) =>
                {
                    Logger.Warning(
                        exception,
                        "Retry {RetryAttempt} after {Delay}s",
                        retryAttempt,
                        timespan.TotalSeconds);
                });
    }
}
