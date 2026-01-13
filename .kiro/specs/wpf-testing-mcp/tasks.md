# Implementation Tasks: WPF Testing MCP Server

## Overview

This document breaks down the implementation into discrete, manageable tasks. Each task references specific requirements and design components.

**Legend**:
- `[ ]` - Not started
- `[x]` - Completed
- `*` - Optional task (can be deferred)
- `🔍` - Testing task
- `📋` - Checkpoint task

---

## Phase 1: Core Infrastructure

### Task 1.1: Setup Project Structure
**Requirements**: All
**Estimated Time**: 30 minutes

- [x] Create solution file `WpfTestingMcp.sln`
- [x] Create `WpfTestingMcp.Core` class library project (.NET 8)
- [x] Create `WpfTestingMcp.Server` console app project (.NET 8)
- [x] Create `WpfTestingMcp.Tests` xUnit test project (.NET 8)
- [x] Add project references (Server → Core, Tests → Core)
- [x] Add NuGet packages:
  - FlaUI.Core 4.0.0
  - FlaUI.UIA3 4.0.0
  - System.Drawing.Common 8.0.0
  - Microsoft.Extensions.DependencyInjection 8.0.0
- [x] Create folder structure in Core:
  - `Automation/`
  - `Debugging/`
  - `Screenshot/`
  - `Safety/`
  - `Session/`
  - `Models/`
  - `Interfaces/`

**Acceptance**: All projects build successfully, folder structure created

---

### Task 1.2: Define Core Interfaces
**Requirements**: All
**Design**: Component Interfaces
**Estimated Time**: 1 hour

- [x] Create `Interfaces/ISafetyService.cs`
  - Define `ValidationResult ValidateAction(string action, string target)`
  - Define `ValidationResult ValidateTextInput(string text)`
  - Define `ValidationResult ValidateProcessName(string processName)`
- [x] Create `Interfaces/ISessionManager.cs`
  - Define `SessionResult CreateSession(string processName, int timeout)`
  - Define `AppSession? GetSession(string sessionId)`
  - Define `bool CloseSession(string sessionId)`
  - Define `List<SessionInfo> GetActiveSessions()`
- [x] Create `Models/ValidationResult.cs`
  - Properties: Status (enum), Message
  - Enum: ValidationStatus (Allowed, Warning, Denied)
- [x] Create `Models/SessionResult.cs`
  - Properties: Success, ErrorMessage, SessionId, ProcessId, ProcessName, WindowTitle
- [x] Create `Models/ActionResult.cs`
  - Properties: Success, Message, Warning, Status (enum)
  - Enum: ActionStatus (Success, Error, Denied)

**Acceptance**: All interfaces compile, models have XML documentation

---

### Task 1.3: Implement Data Models
**Requirements**: All
**Design**: Data Models
**Estimated Time**: 1 hour

- [x] Create `Models/ElementInfo.cs`
  - Properties: AutomationId, Name, ClassName, ControlType, IsEnabled, IsVisible, BoundingRectangle
- [x] Create `Models/TreeNode.cs`
  - Properties: AutomationId, Name, ClassName, ControlType, IsEnabled, IsVisible, Depth, Children (List<TreeNode>)
- [x] Create `Models/SessionInfo.cs`
  - Properties: SessionId, ProcessName, CreatedAt, LastAccessedAt, DurationSeconds, CachedElementsCount
- [x] Create `Models/ConnectResult.cs`
  - Properties: Success, ErrorMessage, ProcessId, ProcessName, WindowTitle, WindowHandle
- [x] Create `Models/ScreenshotResult.cs`
  - Properties: Success, ErrorMessage, Width, Height, SavePath, Base64Data
- [x] Add XML documentation to all models
- [x] Add nullable reference type annotations

**Acceptance**: All models compile with nullable annotations, XML docs present

---

## Phase 2: Safety Layer

### Task 2.1: Implement SafetyService - Dangerous Element Detection
**Requirements**: 12.1, 12.2, 12.3
**Design**: Safety Layer
**Estimated Time**: 1.5 hours

- [x] Create `Safety/SafetyService.cs` implementing `ISafetyService`
- [x] Define dangerous AutomationIds list:
  - CloseButton, ExitButton, ShutdownButton, DeleteAllButton, FormatButton, ResetButton
- [x] Implement `ValidateAction(string action, string target)`:
  - Check if target in dangerous list → return Denied
  - Check if target contains "Delete", "Remove" (case-insensitive) → return Denied
  - Otherwise → return Allowed
- [x] Add clear error messages in Bahasa Indonesia
- [x] Add XML documentation

**Acceptance**: Dangerous elements correctly denied, clear error messages

---

### Task 2.2: Implement SafetyService - Sensitive Data Detection
**Requirements**: 12.4, 12.5, 12.6, 12.7, 12.8
**Design**: Safety Layer
**Estimated Time**: 1.5 hours

- [x] Define sensitive AutomationIds list:
  - PasswordBox, PasswordTextBox, CreditCardInput, SSNInput, BankAccountInput
- [x] Implement sensitive element detection in `ValidateAction`:
  - Check if target in sensitive list → return Warning
  - Check if target contains "Password", "Secret" (case-insensitive) → return Warning
- [x] Implement `ValidateTextInput(string text)`:
  - Regex for SSN: `\d{3}-\d{2}-\d{4}`
  - Regex for Credit Card: `\d{16}`
  - Regex for Email: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
  - Regex for IP: `(?:\d{1,3}\.){3}\d{1,3}`
  - If match → return Warning with message
- [x] Add unit tests for all patterns

**Acceptance**: Sensitive data correctly detected, warnings returned

---

### Task 2.3: Implement SafetyService - Rate Limiting
**Requirements**: 12.9, 12.10
**Design**: Safety Layer
**Estimated Time**: 2 hours

- [x] Add rate limiting state:
  - Dictionary<string, Queue<DateTime>> to track action timestamps
  - Key: action type (click, type, etc)
  - Value: Queue of timestamps (last 60 seconds)
- [x] Implement rate limit check in `ValidateAction`:
  - Remove timestamps older than 60 seconds
  - If queue count >= 60 → return Denied with rate limit message
  - Otherwise → add current timestamp to queue
- [x] Add configurable rate limit (default 60/minute)
- [x] Add unit tests for rate limiting

**Acceptance**: Rate limiting enforced, max 60 actions/minute

---

### Task 2.4: Implement SafetyService - Process Whitelist
**Requirements**: 1.6, 1.7
**Design**: Safety Layer
**Estimated Time**: 1 hour

- [x] Define process whitelist:
  - Simanis62, notepad, calc, mspaint
- [x] Implement `ValidateProcessName(string processName)`:
  - Check if processName in whitelist → return Allowed
  - Otherwise → return Warning with message "Process not in whitelist but connection allowed"
- [x] Add configurable whitelist (future enhancement)
- [x] Add unit tests

**Acceptance**: Process whitelist validated, warnings for non-whitelisted

---

### 📋 Checkpoint 1: Safety Layer Complete
- [x] All SafetyService methods implemented
- [x] Unit tests passing (target 80% coverage)
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 3: Automation Layer

### Task 3.1: Implement AppConnector
**Requirements**: 1.1, 1.2, 1.3, 1.4, 1.5
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Create `Automation/AppConnector.cs`
- [x] Implement `Connect(string processName, int timeout = 5000)`:
  - Use `Process.GetProcessesByName(processName)` to find process
  - If not found → return error "Process '{name}' tidak ditemukan"
  - If multiple instances → use first one
  - Get main window using FlaUI `Application.GetMainWindow()`
  - If timeout → return timeout error
  - Return ConnectResult with process info
- [x] Implement `GetMainWindow()` to return AutomationElement
- [x] Implement `Dispose()` to cleanup resources
- [x] Add timeout handling with CancellationToken
- [x] Add XML documentation

**Acceptance**: Can connect to running process, timeout handled, clear errors

---

### Task 3.2: Implement ElementFinder - Find by AutomationId
**Requirements**: 2.1, 2.4, 2.6
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Create `Automation/ElementFinder.cs`
- [x] Implement `FindByAutomationId(AutomationElement root, string automationId)`:
  - Use FlaUI `FindFirstDescendant(cf => cf.ByAutomationId(automationId))`
  - Search recursively in visual tree
  - If found → return ElementInfo with properties
  - If not found → return error "Element dengan AutomationId '{id}' tidak ditemukan"
- [x] Implement helper `ToElementInfo(AutomationElement element)`:
  - Extract AutomationId, Name, ClassName, ControlType
  - Extract IsEnabled, IsOffscreen (for IsVisible)
  - Extract BoundingRectangle
- [x] Add retry logic (3 attempts with 100ms delay)
- [x] Add XML documentation

**Acceptance**: Can find element by AutomationId, retry logic works

---

### Task 3.3: Implement ElementFinder - Find by Name and ClassName
**Requirements**: 2.2, 2.3, 2.7
**Design**: Automation Layer
**Estimated Time**: 1.5 hours

- [x] Implement `FindByName(AutomationElement root, string name)`:
  - Use FlaUI `FindFirstDescendant(cf => cf.ByName(name))`
  - Return ElementInfo or error
- [x] Implement `FindByClassName(AutomationElement root, string className)`:
  - Use FlaUI `FindFirstDescendant(cf => cf.ByClassName(className))`
  - Return ElementInfo or error
- [x] Implement `FindAllByControlType(AutomationElement root, string controlType)`:
  - Use FlaUI `FindAllDescendants(cf => cf.ByControlType(controlType))`
  - Return List<ElementInfo>
- [x] Add unit tests with mock elements

**Acceptance**: Can find by Name, ClassName, ControlType

---

### Task 3.4: Implement ActionExecutor - Click
**Requirements**: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Create `Automation/ActionExecutor.cs` with ISafetyService dependency
- [x] Implement `Click(AutomationElement element, string? automationId = null)`:
  - Validate with SafetyService.ValidateAction("click", automationId)
  - If denied → return ActionResult with Denied status
  - Check IsEnabled → if false, return error "Element is not enabled"
  - Check IsOffscreen → if true, return error "Element is not visible"
  - Use FlaUI Invoke pattern or Click() method
  - Return ActionResult with success message
- [x] Implement `ClickAt(AutomationElement element, int x, int y)` for coordinate clicks*
- [x] Add error handling with try-catch
- [x] Add XML documentation

**Acceptance**: Can click enabled elements, validation works, dangerous elements denied

---

### Task 3.5: Implement ActionExecutor - Type Text
**Requirements**: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Implement `TypeText(AutomationElement element, string text, string? automationId = null)`:
  - Validate with SafetyService.ValidateAction("type", automationId)
  - Validate text with SafetyService.ValidateTextInput(text)
  - If warnings → include in ActionResult.Warning
  - Check IsEnabled → if false, return error
  - Focus element using `SetFocus()`
  - Clear existing text using Value pattern or Ctrl+A + Delete
  - Type text using FlaUI `Keyboard.Type(text)`
  - Return ActionResult with character count
- [x] Add support for special characters and unicode
- [x] Add unit tests

**Acceptance**: Can type text, sensitive data warnings work, text cleared before typing

---

### Task 3.6: Implement ActionExecutor - Press Keys
**Requirements**: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Implement `PressKey(string key)`:
  - Parse key string (e.g., "Enter", "Tab", "Escape")
  - Map to FlaUI VirtualKeyShort enum
  - Use FlaUI `Keyboard.Press(key)`
  - Add 50ms delay between down and up
  - Return ActionResult
- [x] Implement `PressKeyCombination(string[] keys)`:
  - Validate combination (deny Alt+F4)
  - Hold all keys in sequence
  - Release all keys in reverse sequence
  - Add 100ms delay between keys
- [x] Add dangerous key combination detection
- [x] Add unit tests

**Acceptance**: Can press single keys and combinations, dangerous combos denied

---

### Task 3.7: Implement ActionExecutor - Scroll
**Requirements**: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8
**Design**: Automation Layer
**Estimated Time**: 1.5 hours

- [x] Implement `Scroll(AutomationElement element, string direction)`:
  - Check if element supports Scroll pattern
  - If not → return error "Element does not support scrolling"
  - Parse direction: Up, Down, Left, Right
  - For Up → `ScrollVertical(SmallDecrement)`
  - For Down → `ScrollVertical(SmallIncrement)`
  - For Left → `ScrollHorizontal(SmallDecrement)`
  - For Right → `ScrollHorizontal(SmallIncrement)`
  - Return ActionResult
- [x] Add unit tests with mock scroll pattern

**Acceptance**: Can scroll in all directions, unsupported elements return error

---

### Task 3.8: Implement ActionExecutor - Get/Set Value
**Requirements**: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Implement `GetValue(AutomationElement element)`:
  - Try Value pattern first → return Value property
  - If not available, try Text pattern → return Text property
  - If not available, fallback to Name property
  - Return ActionResult with value
- [x] Implement `SetValue(AutomationElement element, string value, string? automationId = null)`:
  - Validate with SafetyService.ValidateTextInput(value)
  - Check if element is read-only
  - If read-only → return error "Element is read-only"
  - Use Value pattern SetValue() method
  - Return ActionResult
- [x] Add unit tests

**Acceptance**: Can get/set values, read-only check works, pattern fallback works

---

### Task 3.9: Implement ActionExecutor - Wait
**Requirements**: 13.1, 13.2, 13.3, 13.4, 13.6
**Design**: Automation Layer
**Estimated Time**: 1 hour

- [x] Implement `Wait(int milliseconds)`:
  - Validate duration between 0 and 60000ms
  - If invalid → return error "Wait duration must be between 0 and 60000ms"
  - Use `Task.Delay(milliseconds)`
  - Return ActionResult with success message
- [x] Implement `WaitForElement(AutomationElement root, string automationId, int timeout = 5000)`*:
  - Poll FindByAutomationId until found or timeout
  - Return element or timeout error
- [x] Add unit tests

**Acceptance**: Wait works with correct duration, validation enforced

---

### 📋 Checkpoint 2: Automation Layer Complete
- [x] All AppConnector, ElementFinder, ActionExecutor methods implemented
- [x] Unit tests passing (target 80% coverage)
- [x] Integration test: Connect → Find → Click → Type workflow
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 4: Debugging Layer

### Task 4.1: Implement PropertyInspector - Inspect All Properties
**Requirements**: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9
**Design**: Debugging Layer
**Estimated Time**: 2.5 hours

- [x] Create `Debugging/PropertyInspector.cs`
- [x] Implement `InspectAllProperties(AutomationElement element)`:
  - Return Dictionary<string, object?> with all properties
  - Basic: AutomationId, Name, ClassName, ControlType, LocalizedControlType
  - State: IsEnabled, IsOffscreen, IsKeyboardFocusable, HasKeyboardFocus
  - Layout: BoundingRectangle (X, Y, Width, Height)
  - Value pattern (if available): Value, IsReadOnly
  - Text pattern (if available): Text
  - Selection pattern (if available): CanSelectMultiple, IsSelectionRequired
  - Toggle pattern (if available): ToggleState
  - Window pattern (if available): WindowVisualState, WindowInteractionState, IsModal, IsTopmost
- [x] Handle missing patterns gracefully (return null for unavailable)
- [x] Add XML documentation

**Acceptance**: All available properties returned, missing patterns handled

---

### Task 4.2: Implement PropertyInspector - Get Specific Property
**Requirements**: 9.10
**Design**: Debugging Layer
**Estimated Time**: 1 hour

- [x] Implement `GetProperty(AutomationElement element, string propertyName)`:
  - Use reflection or switch statement to get specific property
  - Return property value or null if not available
  - Return error if property name invalid
- [x] Add unit tests for all property names

**Acceptance**: Can get specific properties, invalid names return error

---

### Task 4.3: Implement PropertyInspector - Wait for Property
**Requirements**: 9.11, 9.12, 9.13
**Design**: Debugging Layer
**Estimated Time**: 2 hours

- [x] Implement `WaitForProperty(AutomationElement element, string propertyName, object expectedValue, int timeout = 5000)`:
  - Poll property every 100ms
  - Compare with expectedValue
  - If match → return success with elapsed time
  - If timeout → return timeout error with current value
- [x] Add support for comparison operators (equals, contains, greater than)*
- [x] Add unit tests with mock elements

**Acceptance**: Can wait for property changes, timeout handled

---

### Task 4.4: Implement PropertyInspector - Get Available Patterns
**Requirements**: 14.1, 14.2, 14.3, 14.4, 14.5
**Design**: Debugging Layer
**Estimated Time**: 1.5 hours

- [x] Implement `GetAvailablePatterns(AutomationElement element)`:
  - Check all common patterns:
    - Invoke, Value, Text, Selection, SelectionItem, Toggle, Window
    - Scroll, ScrollItem, ExpandCollapse, Grid, GridItem, Table, TableItem
    - Transform, RangeValue
  - Return List<string> of pattern names
  - If no patterns → return empty list
- [x] Add unit tests

**Acceptance**: All available patterns returned, empty list for no patterns

---

### Task 4.5: Implement VisualTreeNavigator - Get Children
**Requirements**: 10.1, 10.2
**Design**: Debugging Layer
**Estimated Time**: 2 hours

- [x] Create `Debugging/VisualTreeNavigator.cs`
- [x] Implement `GetChildren(AutomationElement element, int depth = 1)`:
  - Get direct children using FlaUI `FindAllChildren()`
  - If depth > 1, recursively get children of children
  - Limit max depth to 5 (prevent performance issues)
  - Return List<TreeNode> with hierarchy
- [x] Implement helper `ToTreeNode(AutomationElement element, int depth)`:
  - Extract AutomationId, Name, ClassName, ControlType, IsEnabled, IsVisible
  - Set Depth property
  - Recursively populate Children if depth > 0
- [x] Add unit tests

**Acceptance**: Can get children recursively, depth limit enforced

---

### Task 4.6: Implement VisualTreeNavigator - Get Parent and Siblings
**Requirements**: 10.3, 10.4, 10.5
**Design**: Debugging Layer
**Estimated Time**: 1.5 hours

- [x] Implement `GetParent(AutomationElement element)`:
  - Use FlaUI `Parent` property
  - If no parent (root) → return error "Element has no parent"
  - Return TreeNode
- [x] Implement `GetSiblings(AutomationElement element)`:
  - Get parent element
  - Get all children of parent
  - Filter out current element
  - Return List<TreeNode>
- [x] Add unit tests

**Acceptance**: Can get parent and siblings, root element handled

---

### Task 4.7: Implement VisualTreeNavigator - Get Full Tree
**Requirements**: 10.6, 10.7, 10.8
**Design**: Debugging Layer
**Estimated Time**: 1.5 hours

- [x] Implement `GetTree(AutomationElement root, int maxDepth = 3)`:
  - Recursively build tree structure
  - Limit depth to prevent performance issues (max 5)
  - Return TreeNode with full hierarchy
- [x] Add performance optimization (cache nodes)*
- [x] Add unit tests

**Acceptance**: Can get full tree, depth limit enforced, performance acceptable

---

### 📋 Checkpoint 3: Debugging Layer Complete
- [x] All PropertyInspector and VisualTreeNavigator methods implemented
- [x] Unit tests passing (target 80% coverage)
- [x] Integration test: Inspect properties and navigate tree
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 5: Screenshot Layer

### Task 5.1: Implement ScreenshotCapture - Capture Element
**Requirements**: 8.1, 8.4, 8.5, 8.6, 8.7
**Design**: Screenshot Layer
**Estimated Time**: 2 hours

- [x] Create `Screenshot/ScreenshotCapture.cs`
- [x] Implement `CaptureElement(AutomationElement element, string? savePath = null)`:
  - Get element's BoundingRectangle
  - Use System.Drawing.Bitmap to capture region
  - If savePath provided → save as PNG file
  - If savePath not provided → convert to base64 string
  - Create directory if not exists
  - Return ScreenshotResult with width, height, path/base64
- [x] Add error handling for invalid paths
- [x] Add XML documentation

**Acceptance**: Can capture element screenshot, save to file or return base64

---

### Task 5.2: Implement ScreenshotCapture - Capture Window and Screen
**Requirements**: 8.2, 8.3
**Design**: Screenshot Layer
**Estimated Time**: 1.5 hours

- [x] Implement `CaptureWindow(AutomationElement window, string? savePath = null)`:
  - Get window's BoundingRectangle
  - Capture entire window region
  - Save or return base64
- [x] Implement `CaptureScreen(string? savePath = null)`:
  - Get primary screen bounds using `Screen.PrimaryScreen.Bounds`
  - Capture entire screen
  - Save or return base64
- [x] Add unit tests

**Acceptance**: Can capture window and screen, save or return base64

---

### Task 5.3: Implement ScreenshotCapture - Compare Screenshots
**Requirements**: 8.8
**Design**: Screenshot Layer
**Estimated Time**: 2 hours

- [x] Implement `CompareScreenshots(string path1, string path2, double threshold = 0.95)`:
  - Load both images as Bitmap
  - Compare dimensions → if different, return false
  - Compare pixel-by-pixel
  - Calculate similarity percentage
  - If similarity >= threshold → return true
  - Return comparison result with similarity score
- [x] Add support for comparing base64 strings*
- [x] Add unit tests with sample images

**Acceptance**: Can compare screenshots, threshold works, similarity calculated

---

### 📋 Checkpoint 4: Screenshot Layer Complete
- [x] All ScreenshotCapture methods implemented
- [x] Unit tests passing (target 80% coverage)
- [x] Integration test: Capture and compare screenshots
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 6: Session Management

### Task 6.1: Implement AppSession
**Requirements**: 11.1, 11.4, 11.5
**Design**: Session Management Layer
**Estimated Time**: 1.5 hours

- [x] Create `Session/AppSession.cs` implementing IDisposable
- [x] Add properties:
  - SessionId (string, GUID)
  - ProcessName (string)
  - Connector (AppConnector)
  - CreatedAt (DateTime)
  - LastAccessedAt (DateTime)
  - CachedElements (Dictionary<string, AutomationElement>)
- [x] Implement `GetInfo()` to return SessionInfo
- [x] Implement `Dispose()` to cleanup connector and cached elements
- [x] Add XML documentation

**Acceptance**: AppSession stores state, Dispose cleans up resources

---

### Task 6.2: Implement SessionManager - Create and Get Session
**Requirements**: 11.1, 11.2, 11.3, 11.4
**Design**: Session Management Layer
**Estimated Time**: 2 hours

- [x] Create `Session/SessionManager.cs` implementing ISessionManager
- [x] Add private field: `Dictionary<string, AppSession> _sessions`
- [x] Add private field: `ISafetyService _safetyService`
- [x] Implement `CreateSession(string processName, int timeout = 5000)`:
  - Validate process name with SafetyService
  - Check if max sessions (5) reached → return error
  - Generate unique session ID (GUID)
  - Create AppConnector and connect to process
  - If connection fails → return error
  - Create AppSession and add to dictionary
  - Return SessionResult with session info
- [x] Implement `GetSession(string sessionId)`:
  - Lookup session in dictionary
  - If found → update LastAccessedAt and return session
  - If not found → return null
- [x] Add XML documentation

**Acceptance**: Can create and get sessions, max sessions enforced

---

### Task 6.3: Implement SessionManager - Close and Cleanup
**Requirements**: 11.6, 11.7
**Design**: Session Management Layer
**Estimated Time**: 2 hours

- [x] Implement `CloseSession(string sessionId)`:
  - Lookup session in dictionary
  - If found → dispose session and remove from dictionary
  - Return true if closed, false if not found
- [x] Implement `GetActiveSessions()`:
  - Return List<SessionInfo> for all active sessions
- [x] Implement auto-cleanup background task:
  - Run every 5 minutes
  - Check LastAccessedAt for all sessions
  - If inactive > 30 minutes → close session
- [x] Implement `Dispose()` to cleanup all sessions and stop background task
- [x] Add unit tests

**Acceptance**: Can close sessions, auto-cleanup works, all sessions disposed on shutdown

---

### 📋 Checkpoint 5: Session Management Complete
- [x] All SessionManager methods implemented
- [x] Unit tests passing (target 80% coverage)
- [x] Integration test: Create multiple sessions, auto-cleanup
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 7: MCP Server Implementation

### Task 7.1: Setup MCP Server Infrastructure
**Requirements**: All
**Design**: MCP Protocol Handler Layer
**Estimated Time**: 2 hours

- [x] Create `WpfTestingMcp.Server/Program.cs`
- [x] Setup stdio communication (Console.In, Console.Out)
- [x] Setup JSON-RPC message parsing
- [x] Setup Dependency Injection container:
  - Register ISafetyService → SafetyService (singleton)
  - Register ISessionManager → SessionManager (singleton)
  - Register all tool implementations (transient)
- [x] Setup graceful shutdown handling
- [x] Add error logging to stderr
- [x] Add XML documentation

**Acceptance**: Server starts, reads from stdin, writes to stdout, DI configured

---

### Task 7.2: Implement MCP Protocol Handler
**Requirements**: All
**Design**: MCP Protocol Handler Layer
**Estimated Time**: 3 hours

- [x] Create `WpfTestingMcp.Server/McpServer.cs`
- [x] Implement MCP protocol methods:
  - `initialize` - Return server info and capabilities
  - `tools/list` - Return list of all available tools
  - `tools/call` - Route to appropriate tool and execute
- [x] Implement request parsing:
  - Parse JSON-RPC request from stdin
  - Extract method and params
  - Validate request format
- [x] Implement response formatting:
  - Format result as JSON-RPC response
  - Write to stdout
  - Flush immediately
- [x] Implement error handling:
  - Catch exceptions from tools
  - Format as JSON-RPC error response
  - Include error code and message
- [x] Add XML documentation

**Acceptance**: MCP protocol implemented, requests parsed, responses formatted

---

### Task 7.3: Implement Tool Base Class
**Requirements**: All
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/IMcpTool.cs` interface
  - Define `string Name { get; }`
  - Define `string Description { get; }`
  - Define `object InputSchema { get; }`
  - Define `Task<object> ExecuteAsync(Dictionary<string, object> args)`
- [x] Create `WpfTestingMcp.Server/Tools/McpToolBase.cs` abstract class
  - Implement common validation logic
  - Implement error handling wrapper
  - Add helper methods for argument extraction
- [x] Add XML documentation

**Acceptance**: Tool interface defined, base class provides common functionality

---

### Task 7.4: Implement ConnectAppTool
**Requirements**: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
**Design**: Tool Registry Layer
**Estimated Time**: 2 hours

- [x] Create `WpfTestingMcp.Server/Tools/ConnectAppTool.cs` implementing IMcpTool
- [x] Define input schema:
  - processName (string, required)
  - timeout (number, optional, default 5000)
- [x] Implement `ExecuteAsync`:
  - Extract processName and timeout from args
  - Call SessionManager.CreateSession()
  - Return SessionResult as JSON
- [x] Add error handling
- [x] Add XML documentation
- [x] Add unit tests

**Acceptance**: Tool connects to app, returns session info, errors handled

---

### Task 7.5: Implement FindElementTool
**Requirements**: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8
**Design**: Tool Registry Layer
**Estimated Time**: 2 hours

- [x] Create `WpfTestingMcp.Server/Tools/FindElementTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - automationId (string, optional)
  - name (string, optional)
  - className (string, optional)
  - controlType (string, optional)
- [x] Implement `ExecuteAsync`:
  - Get session from SessionManager
  - Get main window from session
  - Call ElementFinder with appropriate criteria
  - Cache found element in session
  - Return ElementInfo as JSON
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool finds elements, caches in session, returns element info

---

### Task 7.6: Implement ClickElementTool
**Requirements**: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/ClickElementTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required) - from cached elements
  - x (number, optional) - for coordinate clicks*
  - y (number, optional) - for coordinate clicks*
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call ActionExecutor.Click()
  - Return ActionResult as JSON
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool clicks elements, validation works, errors handled

---

### Task 7.7: Implement TypeTextTool
**Requirements**: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/TypeTextTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - text (string, required)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call ActionExecutor.TypeText()
  - Return ActionResult with warnings if any
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool types text, sensitive data warnings work

---

### Task 7.8: Implement PressKeyTool
**Requirements**: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/PressKeyTool.cs`
- [x] Define input schema:
  - key (string, required) - single key or combination (e.g., "Enter", "Ctrl+C")
- [x] Implement `ExecuteAsync`:
  - Parse key string
  - If single key → call ActionExecutor.PressKey()
  - If combination → call ActionExecutor.PressKeyCombination()
  - Return ActionResult
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool presses keys and combinations, dangerous combos denied

---

### Task 7.9: Implement ScrollElementTool
**Requirements**: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8
**Design**: Tool Registry Layer
**Estimated Time**: 1 hour

- [x] Create `WpfTestingMcp.Server/Tools/ScrollElementTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - direction (string, required) - Up, Down, Left, Right
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call ActionExecutor.Scroll()
  - Return ActionResult
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool scrolls elements, unsupported elements return error

---

### Task 7.10: Implement GetValueTool and SetValueTool
**Requirements**: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/GetValueTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call ActionExecutor.GetValue()
  - Return ActionResult with value
- [x] Create `WpfTestingMcp.Server/Tools/SetValueTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - value (string, required)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call ActionExecutor.SetValue()
  - Return ActionResult
- [x] Add unit tests

**Acceptance**: Tools get and set values, read-only check works

---

### Task 7.11: Implement GetScreenshotTool
**Requirements**: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/GetScreenshotTool.cs`
- [x] Define input schema:
  - sessionId (string, optional) - for element/window capture
  - elementId (string, optional) - for element capture
  - captureType (string, required) - element, window, screen
  - savePath (string, optional)
- [x] Implement `ExecuteAsync`:
  - Based on captureType, call appropriate ScreenshotCapture method
  - Return ScreenshotResult with path or base64
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool captures screenshots, saves or returns base64

---

### Task 7.12: Implement CompareScreenshotsTool*
**Requirements**: 8.8
**Design**: Tool Registry Layer
**Estimated Time**: 1 hour

- [x] Create `WpfTestingMcp.Server/Tools/CompareScreenshotsTool.cs`
- [x] Define input schema:
  - path1 (string, required)
  - path2 (string, required)
  - threshold (number, optional, default 0.95)
- [x] Implement `ExecuteAsync`:
  - Call ScreenshotCapture.CompareScreenshots()
  - Return comparison result with similarity score
- [x] Add unit tests

**Acceptance**: Tool compares screenshots, threshold works

---

### Task 7.13: Implement GetElementPropertiesTool
**Requirements**: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/GetElementPropertiesTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - propertyName (string, optional) - for specific property
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - If propertyName provided → call PropertyInspector.GetProperty()
  - Otherwise → call PropertyInspector.InspectAllProperties()
  - Return properties as JSON
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool returns all or specific properties

---

### Task 7.14: Implement WaitForPropertyTool
**Requirements**: 9.11, 9.12, 9.13
**Design**: Tool Registry Layer
**Estimated Time**: 1.5 hours

- [x] Create `WpfTestingMcp.Server/Tools/WaitForPropertyTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - propertyName (string, required)
  - expectedValue (any, required)
  - timeout (number, optional, default 5000)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call PropertyInspector.WaitForProperty()
  - Return result with elapsed time or timeout error
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool waits for property changes, timeout handled

---

### Task 7.15: Implement NavigateVisualTreeTool
**Requirements**: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8
**Design**: Tool Registry Layer
**Estimated Time**: 2 hours

- [x] Create `WpfTestingMcp.Server/Tools/NavigateVisualTreeTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
  - direction (string, required) - children, parent, siblings, tree
  - depth (number, optional, default 1, max 5)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Based on direction:
    - children → call VisualTreeNavigator.GetChildren()
    - parent → call VisualTreeNavigator.GetParent()
    - siblings → call VisualTreeNavigator.GetSiblings()
    - tree → call VisualTreeNavigator.GetTree()
  - Return TreeNode or List<TreeNode> as JSON
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool navigates tree in all directions, depth limit enforced

---

### Task 7.16: Implement GetAvailablePatternsTool
**Requirements**: 14.1, 14.2, 14.3, 14.4, 14.5
**Design**: Tool Registry Layer
**Estimated Time**: 1 hour

- [x] Create `WpfTestingMcp.Server/Tools/GetAvailablePatternsTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
  - elementId (string, required)
- [x] Implement `ExecuteAsync`:
  - Get session and cached element
  - Call PropertyInspector.GetAvailablePatterns()
  - Return List<string> as JSON
- [x] Add error handling
- [x] Add unit tests

**Acceptance**: Tool returns available patterns

---

### Task 7.17: Implement WaitTool
**Requirements**: 13.1, 13.2, 13.3, 13.4
**Design**: Tool Registry Layer
**Estimated Time**: 30 minutes

- [x] Create `WpfTestingMcp.Server/Tools/WaitTool.cs`
- [x] Define input schema:
  - milliseconds (number, required, min 0, max 60000)
- [x] Implement `ExecuteAsync`:
  - Call ActionExecutor.Wait()
  - Return ActionResult
- [x] Add unit tests

**Acceptance**: Tool waits for specified duration, validation works

---

### Task 7.18: Implement ListSessionsTool
**Requirements**: 11.8
**Design**: Tool Registry Layer
**Estimated Time**: 30 minutes

- [x] Create `WpfTestingMcp.Server/Tools/ListSessionsTool.cs`
- [x] Define input schema: (none)
- [x] Implement `ExecuteAsync`:
  - Call SessionManager.GetActiveSessions()
  - Return List<SessionInfo> as JSON
- [x] Add unit tests

**Acceptance**: Tool lists all active sessions

---

### Task 7.19: Implement CloseSessionTool
**Requirements**: 11.7
**Design**: Tool Registry Layer
**Estimated Time**: 30 minutes

- [x] Create `WpfTestingMcp.Server/Tools/CloseSessionTool.cs`
- [x] Define input schema:
  - sessionId (string, required)
- [x] Implement `ExecuteAsync`:
  - Call SessionManager.CloseSession()
  - Return success/failure result
- [x] Add unit tests

**Acceptance**: Tool closes sessions

---

### 📋 Checkpoint 6: MCP Server Complete
- [x] All 19 tools implemented
- [x] MCP protocol handler working
- [x] Unit tests passing for all tools (target 80% coverage)
- [x] Integration test: Full workflow via MCP protocol
- [x] XML documentation complete
- [x] Code review completed

---

## Phase 8: Testing & Quality Assurance

### Task 8.1: Unit Tests - Safety Layer
**Requirements**: 12.1-12.10
**Design**: Testing Strategy
**Estimated Time**: 3 hours

- [x] 🔍 Test SafetyService.ValidateAction():
  - Test dangerous elements denied (CloseButton, DeleteAllButton, etc)
  - Test dangerous patterns denied (Delete, Remove)
  - Test sensitive elements warned (PasswordBox, etc)
  - Test sensitive patterns warned (Password, Secret)
  - Test allowed elements pass
- [x] 🔍 Test SafetyService.ValidateTextInput():
  - Test SSN pattern detection
  - Test credit card pattern detection
  - Test email pattern detection
  - Test IP address pattern detection
  - Test normal text passes
- [x] 🔍 Test SafetyService rate limiting:
  - Test 60 actions allowed
  - Test 61st action denied
  - Test rate limit reset after 60 seconds
- [x] 🔍 Test SafetyService.ValidateProcessName():
  - Test whitelisted processes allowed
  - Test non-whitelisted processes warned
- [x] Achieve 90%+ coverage for SafetyService

**Acceptance**: All safety validation tests passing, 90%+ coverage

---

### Task 8.2: Unit Tests - Automation Layer
**Requirements**: 1.1-7.8
**Design**: Testing Strategy
**Estimated Time**: 4 hours

- [x] 🔍 Test AppConnector:
  - Test successful connection
  - Test process not found error
  - Test timeout error
  - Test multiple instances handling
- [x] 🔍 Test ElementFinder:
  - Test find by AutomationId
  - Test find by Name
  - Test find by ClassName
  - Test find by ControlType
  - Test element not found error
  - Test retry logic
- [x] 🔍 Test ActionExecutor:
  - Test click enabled element
  - Test click disabled element error
  - Test click dangerous element denied
  - Test type text
  - Test type sensitive data warning
  - Test press key
  - Test press dangerous key combo denied
  - Test scroll
  - Test get/set value
  - Test wait
- [x] Achieve 85%+ coverage for Automation layer

**Acceptance**: All automation tests passing, 85%+ coverage

---

### Task 8.3: Unit Tests - Debugging Layer
**Requirements**: 9.1-10.8, 14.1-14.5
**Design**: Testing Strategy
**Estimated Time**: 3 hours

- [ ] 🔍 Test PropertyInspector:
  - Test inspect all properties
  - Test get specific property
  - Test wait for property
  - Test wait for property timeout
  - Test get available patterns
- [ ] 🔍 Test VisualTreeNavigator:
  - Test get children
  - Test get children recursive
  - Test get parent
  - Test get parent of root error
  - Test get siblings
  - Test get full tree
  - Test depth limit
- [ ] Achieve 85%+ coverage for Debugging layer

**Acceptance**: All debugging tests passing, 85%+ coverage

---

### Task 8.4: Unit Tests - Screenshot Layer
**Requirements**: 8.1-8.8
**Design**: Testing Strategy
**Estimated Time**: 2 hours

- [ ] 🔍 Test ScreenshotCapture:
  - Test capture element
  - Test capture window
  - Test capture screen
  - Test save to file
  - Test return base64
  - Test compare screenshots (identical)
  - Test compare screenshots (different)
  - Test compare screenshots (threshold)
- [ ] Achieve 85%+ coverage for Screenshot layer

**Acceptance**: All screenshot tests passing, 85%+ coverage

---

### Task 8.5: Unit Tests - Session Management
**Requirements**: 11.1-11.8
**Design**: Testing Strategy
**Estimated Time**: 2 hours

- [ ] 🔍 Test SessionManager:
  - Test create session
  - Test max sessions limit
  - Test get session
  - Test close session
  - Test list sessions
  - Test auto-cleanup after 30 minutes
  - Test dispose all sessions
- [ ] 🔍 Test AppSession:
  - Test session info
  - Test cached elements
  - Test dispose
- [ ] Achieve 85%+ coverage for Session layer

**Acceptance**: All session tests passing, 85%+ coverage

---

### Task 8.6: Unit Tests - MCP Tools
**Requirements**: All
**Design**: Testing Strategy
**Estimated Time**: 4 hours

- [ ] 🔍 Test all 19 MCP tools:
  - Test input validation
  - Test successful execution
  - Test error handling
  - Test argument extraction
  - Mock dependencies (SessionManager, SafetyService)
- [ ] Achieve 80%+ coverage for all tools

**Acceptance**: All tool tests passing, 80%+ coverage

---

### Task 8.7: Integration Tests - Full Workflows
**Requirements**: All
**Design**: Testing Strategy
**Estimated Time**: 4 hours

- [ ] 🔍 Create test WPF application with known elements:
  - LoginView with EmailTextBox, PasswordBox, LoginButton
  - DashboardView with WelcomeLabel, LogoutButton
  - DataView with DataGrid, SearchTextBox, SearchButton
- [ ] 🔍 Test Login Workflow:
  - Connect to test app
  - Find email field
  - Type email
  - Find password field
  - Type password
  - Find login button
  - Click login
  - Wait for dashboard
  - Verify dashboard visible
- [ ] 🔍 Test Search Workflow:
  - Navigate to data view
  - Find search field
  - Type search query
  - Click search button
  - Wait for results
  - Verify results visible
- [ ] 🔍 Test Screenshot Workflow:
  - Capture element screenshot
  - Capture window screenshot
  - Compare screenshots
- [ ] 🔍 Test Visual Tree Navigation:
  - Get children of panel
  - Get parent of button
  - Get siblings of textbox
  - Get full tree

**Acceptance**: All integration tests passing, workflows work end-to-end

---

### Task 8.8: Property-Based Tests
**Requirements**: All
**Design**: Correctness Properties
**Estimated Time**: 6 hours

- [ ] 🔍 Setup FsCheck or Hedgehog for property-based testing
- [ ] 🔍 Test Property 1: Connection Idempotence
  - Generate random process names
  - Connect multiple times
  - Verify consistent behavior
- [ ] 🔍 Test Property 2: Element Finding Determinism
  - Generate random AutomationIds
  - Find element multiple times
  - Verify same element returned
- [ ] 🔍 Test Property 3: Action Safety Validation
  - Generate dangerous element IDs
  - Attempt click
  - Verify denied
- [ ] 🔍 Test Property 4: Sensitive Data Detection
  - Generate text with sensitive patterns
  - Attempt type
  - Verify warning
- [ ] 🔍 Test Property 5: Element State Validation
  - Generate disabled elements
  - Attempt click
  - Verify error
- [ ] 🔍 Test Property 6: Screenshot Capture Consistency
  - Capture same element twice
  - Verify >99% similarity
- [ ] 🔍 Test Property 7: Property Inspection Completeness
  - Generate random elements
  - Inspect properties
  - Verify no errors
- [ ] 🔍 Test Property 8: Visual Tree Navigation Consistency
  - Navigate to parent then children
  - Verify original element included
- [ ] 🔍 Test Property 9: Session Timeout Cleanup
  - Create sessions
  - Wait 30+ minutes (simulated)
  - Verify cleanup
- [ ] 🔍 Test Property 10: Rate Limiting Enforcement
  - Perform 61 actions in 1 minute
  - Verify 61st denied
- [ ] 🔍 Test Property 11: Type Text Round Trip
  - Generate random text
  - Type then get value
  - Verify same text
- [ ] 🔍 Test Property 12: Wait Duration Accuracy
  - Generate random durations (0-60000ms)
  - Wait and measure
  - Verify within ±100ms
- [ ] Run each property test with minimum 100 iterations

**Acceptance**: All 12 property tests passing with 100+ iterations each

---

### 📋 Checkpoint 7: Testing Complete
- [ ] All unit tests passing (target 80%+ coverage)
- [ ] All integration tests passing
- [ ] All property-based tests passing (100+ iterations each)
- [ ] Test report generated
- [ ] Code coverage report generated
- [ ] All tests documented

---

## Phase 9: Documentation & Deployment

### Task 9.1: XML Documentation
**Requirements**: All
**Design**: Usability
**Estimated Time**: 2 hours

- [x] Review all public APIs for XML documentation
- [x] Add missing XML docs:
  - Summary for all classes
  - Summary for all public methods
  - Param descriptions for all parameters
  - Returns descriptions
  - Exception descriptions
  - Example usage for complex methods
- [x] Generate XML documentation file
- [x] Verify documentation completeness

**Acceptance**: All public APIs have XML documentation, no warnings

---

### Task 9.2: User Documentation
**Requirements**: All
**Design**: Usability
**Estimated Time**: 3 hours

- [x] Update `README.md` with:
  - Installation instructions
  - Quick start guide
  - Configuration guide (Kiro MCP)
  - Usage examples
  - Troubleshooting section
- [x] Create `TESTING_EXAMPLE.md` with:
  - Login workflow example
  - Search workflow example
  - Screenshot workflow example
  - Visual tree navigation example
- [x] Create `API_REFERENCE.md` with:
  - All 19 tools documented
  - Input schemas
  - Output formats
  - Error codes
- [x] Create `ARCHITECTURE.md` with:
  - High-level architecture diagram
  - Layer responsibilities
  - Component interactions
  - Design decisions

**Acceptance**: All documentation complete, examples work

---

### Task 9.3: Build and Packaging
**Requirements**: All
**Design**: Deployment
**Estimated Time**: 2 hours

- [x] Create build script `build.ps1`:
  - Build Core library (Release)
  - Build Server (Release)
  - Run all tests
  - Generate test report
  - Generate coverage report
- [x] Create publish script `publish.ps1`:
  - Publish single-file executable (win-x64)
  - Copy to `publish/` folder
  - Include README and LICENSE
- [x] Test build on clean machine
- [x] Verify executable runs standalone

**Acceptance**: Build scripts work, single-file executable runs

---

### Task 9.4: Kiro MCP Integration
**Requirements**: All
**Design**: Deployment
**Estimated Time**: 1 hour

- [x] Create MCP configuration template:
  - `mcp-config-template.json`
  - Include all tool names in autoApprove
  - Include environment variables if needed
- [x] Create installation guide:
  - How to add to `.kiro/settings/mcp.json`
  - How to test connection
  - How to verify tools available
- [x] Test integration with Kiro:
  - Add to MCP config
  - Restart Kiro
  - Verify tools listed
  - Test sample workflow

**Acceptance**: MCP integration works, tools available in Kiro

---

### Task 9.5: Performance Testing
**Requirements**: All
**Design**: Performance Considerations
**Estimated Time**: 2 hours

- [x] Create performance test suite:
  - Measure connection time (target < 5s)
  - Measure element finding time (target < 2s)
  - Measure click time (target < 500ms)
  - Measure type text time (target < 1s)
  - Measure screenshot time (target < 1s)
  - Measure property inspection time (target < 500ms)
- [x] Run performance tests on reference machine
- [x] Document performance results
- [x] Identify bottlenecks if targets not met
- [x] Optimize if needed

**Acceptance**: All performance targets met, results documented

---

### Task 9.6: Security Review
**Requirements**: 12.1-12.10
**Design**: Security Considerations
**Estimated Time**: 2 hours

- [x] Review dangerous element detection:
  - Verify all dangerous patterns covered
  - Test with real applications
- [x] Review sensitive data detection:
  - Verify all sensitive patterns covered
  - Test with sample data
- [x] Review rate limiting:
  - Verify enforcement works
  - Test with rapid actions
- [x] Review process whitelist:
  - Verify validation works
  - Test with non-whitelisted processes
- [x] Document security features
- [x] Create security best practices guide

**Acceptance**: Security review complete, no vulnerabilities found

---

### 📋 Checkpoint 8: Documentation & Deployment Complete
- [x] All documentation complete
- [x] Build and packaging working
- [x] Kiro MCP integration tested
- [x] Performance targets met
- [x] Security review passed
- [x] Ready for release

---

## Phase 10: Optional Enhancements

### Task 10.1: Advanced Element Finding*
**Requirements**: 2.8
**Design**: Automation Layer
**Estimated Time**: 2 hours

- [x] Implement `FindAllByControlType()` in ElementFinder
- [x] Implement `FindByXPath()`* for complex queries
- [x] Implement `FindByCondition()`* for custom conditions
- [x] Add caching for frequently searched elements
- [x] Add unit tests

**Acceptance**: Advanced finding methods work, performance improved

---

### Task 10.2: Coordinate-Based Actions*
**Requirements**: 3.8
**Design**: Automation Layer
**Estimated Time**: 1.5 hours

- [x] Implement `ClickAt(x, y)` in ActionExecutor
- [x] Implement `DragAndDrop(from, to)`*
- [x] Implement `HoverAt(x, y)`*
- [x] Add safety validation for coordinates
- [x] Add unit tests

**Acceptance**: Coordinate actions work, validation enforced

---

### Task 10.3: Advanced Screenshot Features*
**Requirements**: 8.8
**Design**: Screenshot Layer
**Estimated Time**: 2 hours

- [x] Implement `CompareScreenshotsBase64()`
- [x] Implement `CaptureRegion(x, y, width, height)`*
- [x] Implement `AnnotateScreenshot()`* for marking elements
- [x] Implement `GenerateVisualDiff()`* for highlighting differences
- [x] Add unit tests

**Acceptance**: Advanced screenshot features work

---

### Task 10.4: Wait for Element*
**Requirements**: 13.6
**Design**: Automation Layer
**Estimated Time**: 1.5 hours

- [x] Implement `WaitForElement()` in ActionExecutor
- [x] Implement `WaitForElementVisible()`*
- [x] Implement `WaitForElementEnabled()`*
- [x] Add configurable polling interval
- [x] Add unit tests

**Acceptance**: Wait for element works, timeout handled

---

### Task 10.5: Batch Operations*
**Design**: Performance Optimization
**Estimated Time**: 3 hours

- [ ] Implement `FindMultipleElements()` for parallel search
- [ ] Implement `ExecuteBatchActions()` for multiple actions
- [ ] Add transaction support (rollback on error)*
- [ ] Add performance benchmarks
- [ ] Add unit tests

**Acceptance**: Batch operations faster than sequential

---

### Task 10.6: Advanced Property Comparison*
**Requirements**: 9.11
**Design**: Debugging Layer
**Estimated Time**: 2 hours

- [ ] Implement comparison operators in `WaitForProperty()`:
  - Equals, NotEquals
  - Contains, NotContains
  - GreaterThan, LessThan
  - Regex match
- [ ] Add unit tests

**Acceptance**: Advanced comparisons work

---

### Task 10.7: Performance Profiling*
**Design**: Performance Optimization
**Estimated Time**: 3 hours

- [ ] Add performance metrics collection:
  - Action execution time
  - Element finding time
  - Screenshot capture time
- [ ] Implement `GetPerformanceMetrics()` tool
- [ ] Add performance dashboard*
- [ ] Add bottleneck detection
- [ ] Add unit tests

**Acceptance**: Performance metrics collected, bottlenecks identified

---

### Task 10.8: Record & Replay*
**Design**: Future Enhancement
**Estimated Time**: 8 hours

- [ ] Implement action recording:
  - Record all actions to JSON file
  - Include timestamps and element info
- [ ] Implement action replay:
  - Parse recorded JSON
  - Execute actions in sequence
  - Handle timing and waits
- [ ] Implement `StartRecording()` tool
- [ ] Implement `StopRecording()` tool
- [ ] Implement `ReplayRecording()` tool
- [ ] Add unit tests

**Acceptance**: Can record and replay user interactions

---

### Task 10.9: Test Report Generation*
**Design**: Future Enhancement
**Estimated Time**: 6 hours

- [ ] Implement test report generator:
  - HTML report with screenshots
  - PDF report with summary
  - Include pass/fail status
  - Include execution time
  - Include error details
- [ ] Implement `GenerateTestReport()` tool
- [ ] Add templates for reports
- [ ] Add unit tests

**Acceptance**: Test reports generated with all info

---

### Task 10.10: CI/CD Integration*
**Design**: Future Enhancement
**Estimated Time**: 4 hours

- [ ] Create GitHub Actions workflow:
  - Build on push
  - Run all tests
  - Generate coverage report
  - Publish artifacts
- [ ] Create Azure Pipelines workflow*
- [ ] Add test result publishing
- [ ] Add coverage badge to README

**Acceptance**: CI/CD pipeline works, tests run automatically

---

## Summary

### Task Statistics

**Total Tasks**: 95 tasks
- **Core Tasks**: 75 tasks (required for MVP)
- **Optional Tasks**: 20 tasks (marked with *)

**Estimated Time**:
- **Core Tasks**: ~120 hours (3 weeks full-time)
- **Optional Tasks**: ~40 hours (1 week full-time)
- **Total**: ~160 hours (4 weeks full-time)

### Phase Breakdown

| Phase | Tasks | Estimated Time | Status |
|-------|-------|----------------|--------|
| Phase 1: Core Infrastructure | 3 | 2.5 hours | Not Started |
| Phase 2: Safety Layer | 4 + Checkpoint | 6 hours | Not Started |
| Phase 3: Automation Layer | 9 + Checkpoint | 17.5 hours | Not Started |
| Phase 4: Debugging Layer | 7 + Checkpoint | 13 hours | Not Started |
| Phase 5: Screenshot Layer | 3 + Checkpoint | 5.5 hours | Not Started |
| Phase 6: Session Management | 3 + Checkpoint | 5.5 hours | Not Started |
| Phase 7: MCP Server | 19 + Checkpoint | 27 hours | Not Started |
| Phase 8: Testing & QA | 8 + Checkpoint | 28 hours | Not Started |
| Phase 9: Documentation & Deployment | 6 + Checkpoint | 12 hours | Not Started |
| Phase 10: Optional Enhancements | 10 | 40 hours | Optional |

### Dependencies

```
Phase 1 (Infrastructure)
    ↓
Phase 2 (Safety) ← Required by Phase 3, 6, 7
    ↓
Phase 3 (Automation) ← Required by Phase 7
    ↓
Phase 4 (Debugging) ← Required by Phase 7
    ↓
Phase 5 (Screenshot) ← Required by Phase 7
    ↓
Phase 6 (Session) ← Required by Phase 7
    ↓
Phase 7 (MCP Server) ← Integrates all layers
    ↓
Phase 8 (Testing) ← Tests all phases
    ↓
Phase 9 (Documentation) ← Documents all phases
    ↓
Phase 10 (Optional) ← Enhancements
```

### Recommended Approach

1. **Week 1**: Phases 1-3 (Infrastructure, Safety, Automation)
   - Focus on core functionality
   - Get basic connect, find, click, type working
   - Checkpoint 1 & 2

2. **Week 2**: Phases 4-6 (Debugging, Screenshot, Session)
   - Add debugging and inspection tools
   - Add screenshot capabilities
   - Add session management
   - Checkpoint 3, 4, 5

3. **Week 3**: Phase 7 (MCP Server)
   - Implement all 19 MCP tools
   - Integrate all layers
   - Test with Kiro
   - Checkpoint 6

4. **Week 4**: Phases 8-9 (Testing, Documentation)
   - Write comprehensive tests
   - Property-based testing
   - Documentation
   - Deployment
   - Checkpoint 7, 8

5. **Week 5** (Optional): Phase 10 (Enhancements)
   - Advanced features
   - Performance optimization
   - Record & replay
   - CI/CD integration

### Success Criteria

**MVP Complete** when:
- [ ] All core tasks (Phases 1-9) completed
- [ ] All 8 checkpoints passed
- [ ] Unit test coverage ≥ 80%
- [ ] All integration tests passing
- [ ] All 12 property-based tests passing (100+ iterations)
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Documentation complete
- [ ] Kiro MCP integration working
- [ ] Can execute full login workflow via Kiro

**Production Ready** when:
- [ ] MVP complete
- [ ] Used in real testing for 2+ weeks
- [ ] No critical bugs
- [ ] Performance stable
- [ ] User feedback incorporated

---

## Next Steps

1. **Review this task list** with team/stakeholders
2. **Prioritize optional tasks** based on business value
3. **Assign tasks** to developers
4. **Setup project tracking** (GitHub Projects, Jira, etc)
5. **Begin Phase 1** - Core Infrastructure

---

**Last Updated**: 2026-01-12
**Version**: 1.0.0
**Status**: Ready for Implementation
**Approved By**: [Pending]

---

## References

- [Requirements Document](.kiro/specs/wpf-testing-mcp/requirements.md)
- [Design Document](.kiro/specs/wpf-testing-mcp/design.md)
- [Project README](tools/wpf-testing-mcp/README.md)
- [SIMANIS62 AGENTS.md](AGENTS.md)
