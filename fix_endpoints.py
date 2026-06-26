import os
import re

api_dir = "/Users/atbhdx/Documents/GitHub/rest-api-for-data-engineering-practice/app/api/v1"

for filename in os.listdir(api_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        filepath = os.path.join(api_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()
            
        # We need to replace:
        # result = await xyz_service.get_multi(...)
        # return StandardResponse(success=True, message="...", data=result)
        # with:
        # return StandardResponse(success=True, message="...", data=result["data"], total_records=result["total_records"], page=result["page"], limit=result["limit"])
        
        # A simpler regex approach:
        # Find: return StandardResponse(success=True, message="(.*?)", data=([a-zA-Z0-9_]+))
        # Replace with: return StandardResponse(success=True, message="\1", data=\2["data"], total_records=\2["total_records"], total_pages=\2["total_pages"], page=\2["page"], limit=\2["limit"])
        
        pattern = r'return StandardResponse\(success=True,\s*message="([^"]+)",\s*data=([a-zA-Z0-9_]+)\)'
        replacement = r'return StandardResponse(success=True, message="\1", data=\2["data"], total_records=\2["total_records"], total_pages=\2["total_pages"], page=\2["page"], limit=\2["limit"])'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"Fixed {filename}")
