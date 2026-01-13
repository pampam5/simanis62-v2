# Design Document: WPF Testing MCP Server

## Overview

WPF Testing MCP Server adalah MCP (Model Context Protocol) server yang memungkinkan AI (Kiro) untuk interact dengan aplikasi WPF secara programmatic. Server ini menyediakan 14 tools untuk connect, find elements, perform actions, inspect properties, capture screenshots, dan navigate visual tree.

### Design Goals

1. **Safety First** - Prevent dangerous actions dan detect sensitive data
2. **Developer Friendly** - Clear error messages, intuitive API
3. **Performance** - Fast operations, efficient caching
4. **Reliability** - Proper error handling, timeout management
5. **Extensibility** - Easy to add new tools dan patterns

### Technology Stack

- **.NET 8** - Modern, performant, cross-platform
- **FlaUI 4.0** - Best-in-class UI Automation library
- **MCP Protocol** - Standard protocol untuk AI tools
- **System.Drawing** - Screenshot capture
- **Dependency Injection** - Testability dan flexibility

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kiro AI Client                           │
│                  (MCP Client via stdio)                     │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol (JSON-RPC over stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              WpfTestingMcp.Server                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           MCP Protocol Handler                       │  │
│  │  - Request parsing                                   │  │
│  │  - Tool routing                                      │  │
│  │  - Response formatting                               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              Tool Registry                           │  │
│  │  - ConnectAppTool                                    │  │
│  │  - FindElementTool                                   │  │
│  │  - ClickElementTool                                  │  │
│  │  - TypeTextTool                                      │  │
│  │  - ... (14 tools total)                              │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              WpfTestingMcp.Core                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Session Management                         │  │
│  │  - SessionManager (multi-session support)           │  │
│  │  - AppSession (connection + cache)                  │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │           Automation Layer                           │  │
│  │  - AppConnector (connect to process)                │  │
│  │  - ElementFinder (find by criteria)                 │  │
│  │  - ActionExecutor (click, type, scroll)             │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │           Debugging Layer                            │  │
│  │  - PropertyInspector (inspect properties)           │  │
│  │  - VisualTreeNavigator (navigate tree)              │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │           Screenshot Layer                           │  │
│  │  - ScreenshotCapture (capture + compare)            │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │           Safety Layer                               │  │
│  │  - SafetyService (validation + rate limiting)       │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    FlaUI Library                            │
│  - UIA3Automation (UI Automation 3.0)                      │
│  - AutomationElement (element wrapper)                     │
│  - Patterns (Invoke, Value, Text, etc)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│            Windows UI Automation API                        │
│  - UIAutomationCore.dll                                    │
│  - UIAutomationClient.dll                                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Simanis62.exe (WPF App)                        │
│  - MainWindow                                              │
│  - Views (Login, Dashboard, Aset, etc)                    │
│  - Controls (Button, TextBox, DataGrid, etc)              │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 1. MCP Protocol Handler Layer
**Responsibility**: Handle MCP protocol communication (JSON-RPC over stdio)

**Components**:
- Request parser (parse JSON-RPC requests)
- Tool router (route to appropriate tool)
- Response formatter (format responses as JSON-RPC)
- Error handler (convert exceptions to MCP errors)

**Why**: Separate protocol handling dari business logic untuk testability

#### 2. Tool Registry Layer
**Responsibility**: Register dan manage all MCP tools

**Components**:
- Tool interface (IMcpTool)
- Tool implementations (ConnectAppTool, FindElementTool, etc)
- Tool metadata (name, description, input schema)

**Why**: Extensible architecture - easy to add new tools

#### 3. Session Management Layer
**Responsibility**: Manage multiple app connections dan element caching

**Components**:
- SessionManager (create, get, close sessions)
- AppSession (session state + cached elements)
- Session cleanup (auto-expire after 30 minutes)

**Why**: Support concurrent testing + performance optimization via caching

#### 4. Automation Layer
**Responsibility**: Core UI automation functionality

**Components**:
- AppConnector (connect to process by name)
- ElementFinder (find elements by criteria)
- ActionExecutor (perform actions with safety checks)

**Why**: Encapsulate FlaUI complexity, provide clean API

#### 5. Debugging Layer
**Responsibility**: Debugging dan inspection tools

**Components**:
- PropertyInspector (inspect properties, wait for changes)
- VisualTreeNavigator (navigate tree structure)

**Why**: Essential untuk debugging UI issues

#### 6. Screenshot Layer
**Responsibility**: Screenshot capture dan comparison

**Components**:
- ScreenshotCapture (capture element/window/screen)
- Screenshot comparison (pixel-by-pixel)

**Why**: Visual testing dan documentation

#### 7. Safety Layer
**Responsibility**: Validate actions dan prevent dangerous operations

**Components**:
- SafetyService (validate actions, detect sensitive data)
- Dangerous element detection
- Sensitive data detection
- Rate limiting

**Why**: Prevent catastrophic actions dalam automated testing

---

## Components and Interfaces

### Core Interfaces

#### ISafetyService
```csharp
public interface ISafetyService
{
    ValidationResult ValidateAction(string action, string target);
    ValidationResult ValidateTextInput(string text);
    ValidationResult ValidateProcessName(string processName);
}
```

**Purpose**: Validate all actions sebelum execution

**Why Interface**: Testability - easy to mock untuk unit tests

#### ISessionManager
```csharp
public interface ISessionManager : IDisposable
{
    SessionResult CreateSession(string processName, int timeout = 5000);
    AppSession? GetSession(string sessionId);
    bool CloseSession(string sessionId);
    List<SessionInfo> GetActiveSessions();
}
```

**Purpose**: Manage multiple app sessions

**Why Interface**: Testability + flexibility (bisa swap implementation)

---

## Data Models

### Session Models

#### AppSession
```csharp
public class AppSession : IDisposable
{
    public string SessionId { get; set; }
    public string ProcessName { get; set; }
    public AppConnector Connector { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime LastAccessedAt { get; set; }
    public Dictionary<string, AutomationElement> CachedElements { get; set; }
    
    public SessionInfo GetInfo();
    public void Dispose();
}
```

**Why Caching**: Performance - avoid re-finding elements

**Why LastAccessedAt**: Auto-cleanup expired sessions

#### SessionInfo
```csharp
public class SessionInfo
{
    public string SessionId { get; set; }
    public string ProcessName { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime LastAccessedAt { get; set; }
    public int DurationSeconds { get; set; }
    public int CachedElementsCount { get; set; }
}
```

**Purpose**: Lightweight session info untuk listing

### Element Models

#### ElementInfo
```csharp
public class ElementInfo
{
    public string? AutomationId { get; set; }
    public string? Name { get; set; }
    public string? ClassName { get; set; }
    public string? ControlType { get; set; }
    public bool IsEnabled { get; set; }
    public bool IsVisible { get; set; }
    public string? BoundingRectangle { get; set; }
}
```

**Purpose**: Serializable element info (AutomationElement tidak serializable)

#### TreeNode
```csharp
public class TreeNode
{
    public string? AutomationId { get; set; }
    public string? Name { get; set; }
    public string? ClassName { get; set; }
    public string? ControlType { get; set; }
    public bool IsEnabled { get; set; }
    public bool IsVisible { get; set; }
    public int Depth { get; set; }
    public List<TreeNode> Children { get; set; }
}
```

**Purpose**: Hierarchical tree representation

**Why Depth**: Limit recursion untuk prevent performance issues

### Result Models

All operations return strongly-typed result objects:

```csharp
// Connection result
public class ConnectResult
{
    public bool Success { get; set; }
    public string? ErrorMessage { get; set; }
    public int ProcessId { get; set; }
    public string? ProcessName { get; set; }
    public string? WindowTitle { get; set; }
    public string? WindowHandle { get; set; }
}

// Action result
public class ActionResult
{
    public bool Success { get; set; }
    public string? Message { get; set; }
    public string? Warning { get; set; }
    public ActionStatus Status { get; set; } // Success, Error, Denied
}

// Validation result
public class ValidationResult
{
    public ValidationStatus Status { get; set; } // Allowed, Warning, Denied
    public string? Message { get; set; }
    
    public bool IsAllowed => Status == ValidationStatus.Allowed;
    public bool IsWarning => Status == ValidationStatus.Warning;
    public bool IsDenied => Status == ValidationStatus.Denied;
}
```

**Why Strongly-Typed**: Type safety, IntelliSense, compile-time checking

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Connection Idempotence
*For any* process name, connecting multiple times should reuse existing session or create new session without errors

**Validates: Requirements 1.1, 1.4**

**Why Important**: Prevent duplicate connections, ensure consistent behavior

### Property 2: Element Finding Determinism
*For any* element with unique AutomationId, finding the element multiple times should return the same element

**Validates: Requirements 2.1, 2.4**

**Why Important**: Consistency dalam element references

### Property 3: Action Safety Validation
*For any* dangerous element (CloseButton, DeleteAllButton), attempting to click should be denied

**Validates: Requirements 3.4, 12.2**

**Why Important**: Prevent catastrophic actions

### Property 4: Sensitive Data Detection
*For any* text containing sensitive patterns (SSN, credit card), typing should trigger warning

**Validates: Requirements 4.4, 12.7**

**Why Important**: Prevent sensitive data exposure

### Property 5: Element State Validation
*For any* disabled element (IsEnabled=false), attempting to click should return error

**Validates: Requirements 3.2**

**Why Important**: Prevent invalid operations

### Property 6: Screenshot Capture Consistency
*For any* element, capturing screenshot twice without UI changes should produce identical images (>99% similarity)

**Validates: Requirements 8.1, 8.8**

**Why Important**: Reliable visual testing

### Property 7: Property Inspection Completeness
*For any* element, inspecting properties should return all available properties without errors

**Validates: Requirements 9.1, 9.2**

**Why Important**: Complete debugging information

### Property 8: Visual Tree Navigation Consistency
*For any* element, navigating to parent then back to children should include the original element

**Validates: Requirements 10.1, 10.3**

**Why Important**: Correct tree structure

### Property 9: Session Timeout Cleanup
*For any* session inactive for >30 minutes, the session should be automatically cleaned up

**Validates: Requirements 11.6**

**Why Important**: Prevent memory leaks

### Property 10: Rate Limiting Enforcement
*For any* action type, performing >60 actions within 1 minute should be denied

**Validates: Requirements 12.10**

**Why Important**: Prevent abuse and infinite loops

### Property 11: Type Text Round Trip
*For any* TextBox element, typing text then getting value should return the same text

**Validates: Requirements 4.6, 7.1**

**Why Important**: Verify text input correctness

### Property 12: Wait Duration Accuracy
*For any* wait duration between 0-60000ms, actual wait time should be within ±100ms of requested duration

**Validates: Requirements 13.1, 13.4**

**Why Important**: Reliable timing for async operations

---

## Error Handling

### Error Categories

#### 1. Connection Errors
- Process not found
- Main window not found
- Connection timeout
- Process not in whitelist

**Handling**: Return clear error message, suggest alternatives

#### 2. Element Not Found Errors
- Element with criteria not found
- Element became stale (app closed/refreshed)

**Handling**: Return error with search criteria, suggest retry

#### 3. Action Validation Errors
- Element disabled
- Element not visible
- Dangerous action denied
- Rate limit exceeded

**Handling**: Return error with reason, suggest fix

#### 4. Operation Errors
- Pattern not supported
- Operation timeout
- Unexpected exception

**Handling**: Return error with details, log for debugging

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "ELEMENT_NOT_FOUND",
    "message": "Element dengan AutomationId 'LoginButton' tidak ditemukan",
    "details": {
      "searchCriteria": "AutomationId",
      "searchValue": "LoginButton",
      "suggestion": "Verify AutomationId is set in XAML"
    }
  }
}
```

**Why Structured**: Easy to parse, actionable information

---

## Testing Strategy

### Unit Testing

**Scope**: Core library components (AppConnector, ElementFinder, ActionExecutor, etc)

**Tools**: xUnit, Moq (for mocking)

**Coverage Target**: 80%

**Example Tests**:
```csharp
[Fact]
public void SafetyService_ValidateAction_DeniesCloseButton()
{
    // Arrange
    var safety = new SafetyService();
    
    // Act
    var result = safety.ValidateAction("click", "CloseButton");
    
    // Assert
    Assert.True(result.IsDenied);
    Assert.Contains("dangerous element", result.Message);
}

[Fact]
public void ElementFinder_FindByAutomationId_ReturnsElement()
{
    // Arrange
    var mockElement = CreateMockElement("LoginButton");
    var finder = new ElementFinder(mockElement);
    
    // Act
    var result = finder.FindByAutomationId("LoginButton");
    
    // Assert
    Assert.True(result.Success);
    Assert.NotNull(result.Element);
}
```

### Integration Testing

**Scope**: End-to-end workflows dengan real WPF app

**Tools**: xUnit, TestStack.White (untuk setup test app)

**Test App**: Simple WPF app dengan known elements

**Example Tests**:
```csharp
[Fact]
public async Task FullWorkflow_LoginFlow_Success()
{
    // Arrange
    var testApp = LaunchTestApp();
    var connector = new AppConnector();
    
    // Act - Connect
    var connectResult = connector.Connect("TestApp");
    Assert.True(connectResult.Success);
    
    // Act - Find email field
    var finder = new ElementFinder(connector.GetMainWindow());
    var emailResult = finder.FindByAutomationId("EmailTextBox");
    Assert.True(emailResult.Success);
    
    // Act - Type email
    var executor = new ActionExecutor(new SafetyService());
    var typeResult = executor.TypeText(emailResult.Element, "test@example.com");
    Assert.True(typeResult.Success);
    
    // Act - Click login
    var loginResult = finder.FindByAutomationId("LoginButton");
    var clickResult = executor.Click(loginResult.Element);
    Assert.True(clickResult.Success);
    
    // Assert - Dashboard visible
    await Task.Delay(1000);
    var dashboardResult = finder.FindByAutomationId("DashboardView");
    Assert.True(dashboardResult.Success);
    Assert.True(dashboardResult.ElementInfo.IsVisible);
}
```

### Property-Based Testing

**Scope**: Correctness properties (see Correctness Properties section)

**Tools**: FsCheck or Hedgehog (property-based testing libraries)

**Configuration**: Minimum 100 iterations per property

**Example**:
```csharp
[Property(Arbitrary = new[] { typeof(Generators) })]
public Property TypeText_RoundTrip_PreservesText(string text)
{
    // Arrange
    var element = CreateTextBoxElement();
    var executor = new ActionExecutor(new SafetyService());
    
    // Act
    executor.TypeText(element, text);
    var result = executor.GetValue(element);
    
    // Assert
    return (result.Value == text).ToProperty();
}
```

---

## Performance Considerations

### Caching Strategy

**Element Caching**: Cache found elements in session
- **Why**: Avoid re-finding elements (expensive operation)
- **Invalidation**: Clear cache on app refresh or element stale

**Session Caching**: Reuse connections
- **Why**: Avoid reconnecting to same app
- **Cleanup**: Auto-expire after 30 minutes

### Optimization Techniques

1. **Lazy Loading**: Only load properties when requested
2. **Parallel Search**: Search multiple criteria in parallel (future enhancement)
3. **Smart Retry**: Retry with exponential backoff for transient errors
4. **Batch Operations**: Support batch element finding (future enhancement)

### Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Connect | < 5s | Time from request to connected |
| Find Element | < 2s | Time from request to element found |
| Click | < 500ms | Time from request to click executed |
| Type Text | < 1s | Time from request to text typed |
| Screenshot | < 1s | Time from request to image captured |
| Inspect | < 500ms | Time from request to properties returned |

---

## Security Considerations

### Process Whitelist

**Default Whitelist**: Simanis62, notepad, calc, mspaint

**Why**: Prevent connection to system processes or malicious apps

**Configuration**: Configurable via settings (future enhancement)

### Dangerous Element Detection

**Dangerous Patterns**:
- AutomationId contains: Close, Exit, Shutdown, Delete, Remove, Format, Reset
- ClassName: CloseButton, ExitButton

**Why**: Prevent accidental app closure or data loss

### Sensitive Data Detection

**Sensitive Patterns**:
- SSN: `\d{3}-\d{2}-\d{4}`
- Credit Card: `\d{16}`
- Email: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
- IP Address: `(?:\d{1,3}\.){3}\d{1,3}`

**Why**: Warn about potential sensitive data exposure

### Rate Limiting

**Limit**: 60 actions per minute per action type

**Why**: Prevent abuse and infinite loops

**Implementation**: Track action timestamps, remove old entries

---

## Deployment

### Build Process

```bash
# Build Core library
dotnet build WpfTestingMcp.Core/WpfTestingMcp.Core.csproj -c Release

# Build Server
dotnet build WpfTestingMcp.Server/WpfTestingMcp.Server.csproj -c Release

# Run tests
dotnet test WpfTestingMcp.Tests/WpfTestingMcp.Tests.csproj

# Publish single-file
dotnet publish WpfTestingMcp.Server/WpfTestingMcp.Server.csproj \
  -c Release \
  -r win-x64 \
  --self-contained \
  -p:PublishSingleFile=true \
  -o publish/
```

### Kiro MCP Configuration

```json
{
  "mcpServers": {
    "wpf-testing": {
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "D:\\simanis62-v2\\tools\\wpf-testing-mcp\\WpfTestingMcp.Server\\WpfTestingMcp.Server.csproj"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "connect_app",
        "find_element",
        "click_element",
        "type_text",
        "get_screenshot",
        "get_element_properties",
        "navigate_visual_tree"
      ]
    }
  }
}
```

### System Requirements

- **OS**: Windows 10/11 (UI Automation requires Windows)
- **.NET**: .NET 8 Runtime
- **Memory**: 100MB minimum
- **Disk**: 50MB for binaries

---

## Future Enhancements

### Phase 2: Advanced Features

1. **Record & Replay**: Record user interactions, generate test scripts
2. **Test Report Generation**: HTML/PDF reports dengan screenshots
3. **CI/CD Integration**: Run tests in Azure Pipelines / GitHub Actions
4. **Performance Profiling**: Detailed metrics, bottleneck detection

### Phase 3: Extended Support

1. **WinForms Support**: Extend to WinForms applications
2. **Win32 Support**: Support legacy Win32 apps
3. **Multi-monitor**: Support multi-monitor setups
4. **Parallel Testing**: Run tests in parallel

### Phase 4: Cloud & Scale

1. **Cloud Testing**: Run tests on cloud VMs
2. **Test Distribution**: Distribute tests across multiple machines
3. **Real-time Collaboration**: Multiple developers testing simultaneously

---

**Last Updated**: 2026-01-12
**Version**: 1.0.0
**Status**: Draft - Ready for Review
