"""
Comprehensive guide to typing **kwargs in Python

This file demonstrates different idiomatic approaches to typing **kwargs in Python,
including their pros, cons, and appropriate use cases.

Author: Claude Code
Date: 2025-08-22
Python Version: 3.8+
"""

import sys
from typing import Any, List, Union, TypeVar, Callable, Optional, Protocol

# Python 3.8+ imports
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

# Python 3.10+ imports
if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

# Python 3.11+ imports
if sys.version_info >= (3, 11):
    from typing import Unpack
else:
    from typing_extensions import Unpack


print(f"Running on Python {sys.version}")
print("=" * 60)


# =============================================================================
# 1. Basic Any Approach
# =============================================================================
print("\n1. BASIC ANY APPROACH")
print("-" * 30)


def basic_any_function(**kwargs: Any) -> str:
    """
    Most basic approach using Any type.

    Pros:
    - Simple and straightforward
    - Works with all Python versions
    - No restrictions on kwargs

    Cons:
    - No type safety
    - No IDE autocompletion
    - No static type checking benefits

    Use when: Prototyping, handling truly dynamic kwargs, or when type safety isn't critical
    """
    return f"Received {len(kwargs)} arguments: {list(kwargs.keys())}"


# Example usage
result1 = basic_any_function(name="John", age=30, city="NYC")
print(f"Result: {result1}")


# =============================================================================
# 2. TypedDict with Unpack (Python 3.11+)
# =============================================================================
print("\n\n2. TYPEDDICT WITH UNPACK (Python 3.11+)")
print("-" * 45)


class UserKwargs(TypedDict):
    """Type definition for user-related kwargs."""

    name: str
    age: int
    email: Optional[str]
    is_active: bool


def typed_dict_function(**kwargs: Unpack[UserKwargs]) -> str:
    """
    Modern approach using TypedDict with Unpack.

    Pros:
    - Excellent type safety
    - Great IDE support and autocompletion
    - Clear documentation of expected arguments
    - Mypy/type checker support

    Cons:
    - Requires Python 3.11+ (or typing_extensions)
    - All kwargs must conform to the TypedDict
    - Less flexible than Any approach

    Use when: You know exactly what kwargs to expect and want strong typing
    """
    name = kwargs.get("name", "Unknown")
    age = kwargs.get("age", 0)
    email = kwargs.get("email", "No email")
    is_active = kwargs.get("is_active", False)

    return f"User: {name}, Age: {age}, Email: {email}, Active: {is_active}"


# Example usage
if sys.version_info >= (3, 11):
    result2 = typed_dict_function(name="Alice", age=25, email="alice@example.com", is_active=True)
    print(f"Result: {result2}")
else:
    print("Skipping - requires Python 3.11+")


# =============================================================================
# 3. Protocol-based Approach
# =============================================================================
print("\n\n3. PROTOCOL-BASED APPROACH")
print("-" * 30)


class ConfigProtocol(Protocol):
    """Protocol defining the interface for configuration objects."""

    debug: bool
    timeout: int
    retries: Optional[int]


def process_with_config(data: str, **config: Any) -> str:
    """
    Function that expects kwargs conforming to ConfigProtocol.

    Pros:
    - Structural typing (duck typing with types)
    - More flexible than TypedDict
    - Works with any object that has the required attributes
    - Good for defining interfaces

    Cons:
    - Less explicit about kwargs structure
    - Requires manual validation or type narrowing
    - Protocol compliance checked at usage, not definition

    Use when: You want structural typing or need to work with different
             object types that share common attributes
    """
    # Type narrowing/validation would typically happen here
    debug = config.get("debug", False)
    timeout = config.get("timeout", 30)
    retries = config.get("retries", 3)

    result = f"Processing '{data}' with debug={debug}, timeout={timeout}, retries={retries}"
    return result


# Example usage
result3 = process_with_config("sample data", debug=True, timeout=60, retries=5)
print(f"Result: {result3}")


# =============================================================================
# 4. ParamSpec for Signature Preservation
# =============================================================================
print("\n\n4. PARAMSPEC FOR SIGNATURE PRESERVATION")
print("-" * 40)

P = ParamSpec("P")
T = TypeVar("T")


def decorator_with_kwargs(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that preserves the original function's signature.

    Pros:
    - Preserves exact function signature
    - Perfect for decorators and wrappers
    - Type checkers understand the signature
    - Maintains parameter names and types

    Cons:
    - More complex syntax
    - Primarily useful for decorators/wrappers
    - Requires understanding of ParamSpec

    Use when: Creating decorators, wrappers, or middleware that should
             preserve the original function signature
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__} with args={len(args)} kwargs={list(kwargs.keys())}")
        return func(*args, **kwargs)

    return wrapper


@decorator_with_kwargs
def greet_user(name: str, greeting: str = "Hello", *, punctuation: str = "!") -> str:
    """Example function to demonstrate ParamSpec."""
    return f"{greeting} {name}{punctuation}"


# Example usage
result4 = greet_user("Bob", greeting="Hi", punctuation=".")
print(f"Result: {result4}")


# =============================================================================
# 5. Specific Typed Kwargs with TypedDict (Backward Compatible)
# =============================================================================
print("\n\n5. SPECIFIC TYPED KWARGS WITH TYPEDDICT (Backward Compatible)")
print("-" * 65)


class DatabaseConfig(TypedDict, total=False):
    """Configuration for database connections. All fields optional."""

    host: str
    port: int
    username: str
    password: str
    ssl: bool
    timeout: int


class RequiredDatabaseConfig(TypedDict):
    """Required database configuration fields."""

    database_name: str


class FullDatabaseConfig(RequiredDatabaseConfig, DatabaseConfig):
    """Combined required and optional database configuration."""

    pass


def connect_to_database(database_name: str, **config: Any) -> str:
    """
    Connect to database with typed configuration.

    This approach works with older Python versions while still providing
    some type safety through documentation and runtime validation.

    Pros:
    - Works with older Python versions
    - Self-documenting through TypedDict
    - Can validate at runtime
    - Flexible - accepts extra kwargs

    Cons:
    - No compile-time type checking for kwargs
    - Requires runtime validation for type safety
    - Less IDE support than Unpack approach

    Use when: Need backward compatibility with older Python versions
             but still want some typing benefits
    """
    # Runtime type validation (optional)
    expected_keys = {"host", "port", "username", "password", "ssl", "timeout"}
    unexpected_keys = set(config.keys()) - expected_keys
    if unexpected_keys:
        print(f"Warning: Unexpected configuration keys: {unexpected_keys}")

    host = config.get("host", "localhost")
    port = config.get("port", 5432)
    ssl = config.get("ssl", False)

    return f"Connected to {database_name} at {host}:{port} (SSL: {ssl})"


# Example usage
result5 = connect_to_database("myapp", host="db.example.com", port=5432, username="admin", ssl=True)
print(f"Result: {result5}")


# =============================================================================
# 6. Union Types for Multiple Possible Kwargs Structures
# =============================================================================
print("\n\n6. UNION TYPES FOR MULTIPLE KWARGS STRUCTURES")
print("-" * 45)


class EmailConfig(TypedDict):
    """Configuration for email notifications."""

    email: str
    smtp_server: str


class WebhookConfig(TypedDict):
    """Configuration for webhook notifications."""

    webhook_url: str
    secret: Optional[str]


NotificationConfig = Union[EmailConfig, WebhookConfig]


def send_notification(message: str, **config: Any) -> str:
    """
    Send notification using either email or webhook configuration.

    Pros:
    - Supports multiple configuration types
    - Clear documentation of alternatives
    - Type-safe when used with proper type narrowing

    Cons:
    - Requires runtime type checking/narrowing
    - More complex logic to handle different config types
    - Union types can be confusing

    Use when: Function can accept different types of configuration
             with mutually exclusive fields
    """
    if "email" in config and "smtp_server" in config:
        # Email configuration
        email = config["email"]
        smtp = config["smtp_server"]
        return f"Sending '{message}' via email to {email} using {smtp}"
    elif "webhook_url" in config:
        # Webhook configuration
        url = config["webhook_url"]
        secret = config.get("secret", "none")
        return f"Sending '{message}' to webhook {url} (secret: {secret})"
    else:
        raise ValueError("Invalid notification configuration")


# Example usage
result6a = send_notification("Hello", email="user@example.com", smtp_server="smtp.gmail.com")
result6b = send_notification("World", webhook_url="https://hooks.example.com/notify", secret="abc123")
print(f"Email result: {result6a}")
print(f"Webhook result: {result6b}")


# =============================================================================
# 7. Generic TypeVar for Flexible Return Types
# =============================================================================
print("\n\n7. GENERIC TYPEVAR FOR FLEXIBLE RETURN TYPES")
print("-" * 42)

R = TypeVar("R")


def process_with_transform(data: str, transform: Callable[[str], R], **options: Any) -> R:
    """
    Process data with a transformation function, passing options as kwargs.

    Pros:
    - Flexible return type based on transform function
    - Preserves type information through the call chain
    - Good for pipeline/functional programming patterns

    Cons:
    - More complex type signature
    - Kwargs are still untyped
    - Requires understanding of TypeVar

    Use when: Building flexible processing pipelines where the return type
             depends on the transformation function
    """
    # Apply any preprocessing based on options
    if options.get("uppercase", False):
        data = data.upper()
    if options.get("strip", True):
        data = data.strip()

    # Apply the transformation
    return transform(data)


# Example usage
def to_length(s: str) -> int:
    return len(s)


def to_words(s: str) -> List[str]:
    return s.split()


result7a = process_with_transform("  hello world  ", to_length, uppercase=True, strip=True)
result7b = process_with_transform("  hello world  ", to_words, strip=True)

print(f"Length result: {result7a} (type: {type(result7a)})")
print(f"Words result: {result7b} (type: {type(result7b)})")


# =============================================================================
# Summary and Recommendations
# =============================================================================
print("\n\n" + "=" * 60)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 60)

recommendations = """
Choose your approach based on these guidelines:

1. **TypedDict + Unpack** (Python 3.11+)
   → Best for new code with known kwargs structure
   → Maximum type safety and IDE support

2. **Basic Any** 
   → Quick prototyping or truly dynamic kwargs
   → When type safety isn't critical

3. **Protocol-based**
   → When you need structural typing
   → Working with objects that share common attributes

4. **ParamSpec**
   → Essential for decorators and function wrappers
   → When preserving exact signatures matters

5. **TypedDict (backward compatible)**
   → Need typing benefits with older Python versions
   → Can add runtime validation

6. **Union types**
   → Multiple possible kwargs structures
   → Mutually exclusive configuration options

7. **Generic TypeVar**
   → Flexible return types in processing pipelines
   → When return type depends on input functions

Remember: Start with the most restrictive typing that works for your use case,
then relax constraints as needed for flexibility.
"""

print(recommendations)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("Run with different Python versions to see compatibility differences.")
