 {
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "resolutionInput",
      "type": "httpTrigger",
      "direction": "in",
      "authLevel": "anonymous",
      "methods": ["post"],
      "route": "store-resolution"
    }
  ]
}
