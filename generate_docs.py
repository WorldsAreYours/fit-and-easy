"""
Generate OpenAPI documentation files for the Personal Trainer App API.
This script creates both JSON and YAML versions of the API specification.
"""

import json
import yaml
from main import app

def generate_openapi_files():
    """Generate OpenAPI specification files"""
    
    # Get the OpenAPI schema
    openapi_schema = app.openapi()
    
    # Write JSON version
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("✅ Generated openapi.json")
    
    # Write YAML version  
    with open("openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, sort_keys=False)
    print("✅ Generated openapi.yaml")
    
    # Print summary
    print(f"\n📊 API Documentation Summary:")
    print(f"   • Title: {openapi_schema['info']['title']}")
    print(f"   • Version: {openapi_schema['info']['version']}")
    print(f"   • Endpoints: {len(openapi_schema['paths'])} paths")
    
    # List all endpoints
    print(f"\n🔗 Available Endpoints:")
    for path, methods in openapi_schema['paths'].items():
        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                summary = details.get('summary', 'No description')
                print(f"   • {method.upper():<6} {path:<35} - {summary}")
    
    print(f"\n📖 How to view documentation:")
    print(f"   • Swagger UI:  http://localhost:8000/docs")
    print(f"   • ReDoc:       http://localhost:8000/redoc")
    print(f"   • OpenAPI JSON: http://localhost:8000/openapi.json")
    print(f"   • Local files: openapi.json, openapi.yaml")

if __name__ == "__main__":
    generate_openapi_files()