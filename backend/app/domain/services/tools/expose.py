"""Expose tool for generating public URLs for local services using cloudflared"""
from typing import Dict, Optional
import uuid
import asyncio
import re
from app.domain.services.tools.base import tool, BaseTool
from app.domain.models.tool_result import ToolResult

class ExposeTool(BaseTool):
    """Expose tool class, providing public URL generation for local services using cloudflared tunnels"""

    name: str = "expose"

    def __init__(self):
        """Initialize Expose tool class"""
        super().__init__()
        # Store active port mappings with process info
        self._port_mappings: Dict[int, Dict[str, any]] = {}
        # Check cloudflared availability
        self._cloudflared_available: Optional[bool] = None

    async def _check_cloudflared(self) -> bool:
        """Check if cloudflared is installed and available

        Returns:
            True if cloudflared is available, False otherwise
        """
        if self._cloudflared_available is not None:
            return self._cloudflared_available

        try:
            process = await asyncio.create_subprocess_exec(
                'which', 'cloudflared',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            self._cloudflared_available = process.returncode == 0
        except Exception:
            self._cloudflared_available = False

        return self._cloudflared_available

    async def _create_cloudflared_tunnel(self, port: int) -> Optional[Dict[str, any]]:
        """Create a cloudflared tunnel for the specified port

        Args:
            port: Port number to expose

        Returns:
            Dictionary with tunnel info (url, process) or None if failed
        """
        try:
            # Start cloudflared tunnel process
            process = await asyncio.create_subprocess_exec(
                'cloudflared', 'tunnel', '--url', f'http://localhost:{port}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for tunnel URL to be generated (max 10 seconds)
            url_pattern = re.compile(r'https://[a-z0-9-]+\.trycloudflare\.com')
            timeout = 10

            async def read_output():
                """Read output until URL is found or timeout"""
                try:
                    while True:
                        line = await asyncio.wait_for(
                            process.stderr.readline(),
                            timeout=1.0
                        )
                        if not line:
                            break

                        line_str = line.decode('utf-8')
                        match = url_pattern.search(line_str)
                        if match:
                            return match.group(0)
                except asyncio.TimeoutError:
                    pass
                return None

            # Try to get URL with timeout
            try:
                url = await asyncio.wait_for(read_output(), timeout=timeout)
                if url:
                    return {
                        "url": url,
                        "process": process,
                        "method": "cloudflared"
                    }
            except asyncio.TimeoutError:
                pass

            # If we couldn't get URL, terminate process
            process.terminate()
            await process.wait()

        except Exception as e:
            pass

        return None

    @tool(
        name="expose_port",
        description=(
            "Generate a public URL for a service running on a specified port using cloudflared tunnels. "
            "The service must bind to 0.0.0.0 (not localhost) to be accessible. "
            "Returns a real public HTTPS URL (e.g., https://xyz.trycloudflare.com) if cloudflared is available, "
            "otherwise returns a mock URL for testing purposes."
        ),
        parameters={
            "port": {
                "type": "integer",
                "description": "Port number where the service is running (1024-65535)"
            },
            "description": {
                "type": "string",
                "description": "Optional description of the service being exposed"
            }
        },
        required=["port"]
    )
    async def expose_port(
        self,
        port: int,
        description: Optional[str] = None
    ) -> ToolResult:
        """Generate public URL for service running on specified port using cloudflared

        Args:
            port: Port number where the service is running (1024-65535)
            description: Optional description of the service

        Returns:
            ToolResult containing the public URL or error message
        """
        # Validate port number
        if not isinstance(port, int) or port < 1024 or port > 65535:
            return ToolResult(
                success=False,
                message="Port must be an integer between 1024 and 65535",
                data=None
            )

        # Check if port is already exposed
        if port in self._port_mappings:
            existing_mapping = self._port_mappings[port]
            return ToolResult(
                success=True,
                message=f"Port {port} is already exposed",
                data={
                    "url": existing_mapping["url"],
                    "port": port,
                    "method": existing_mapping.get("method", "mock"),
                    "description": existing_mapping.get("description"),
                    "status": "existing"
                }
            )

        # Try to use cloudflared if available
        cloudflared_available = await self._check_cloudflared()
        tunnel_info = None

        if cloudflared_available:
            tunnel_info = await self._create_cloudflared_tunnel(port)

        if tunnel_info:
            # Cloudflared tunnel created successfully
            public_url = tunnel_info["url"]
            method = "cloudflared"

            # Store the mapping with process info
            self._port_mappings[port] = {
                "url": public_url,
                "process": tunnel_info["process"],
                "method": method,
                "description": description or f"Service on port {port}",
                "port": str(port)
            }

            msg_parts = [
                f"✅ Successfully exposed port {port} using cloudflared",
                f"🌐 Public URL: {public_url}",
            ]

            if description:
                msg_parts.insert(1, f"📝 Service: {description}")

            msg_parts.extend([
                "",
                "⚠️  Important:",
                "  • Ensure your application binds to 0.0.0.0 (not localhost)",
                "  • The tunnel will remain active until explicitly stopped",
                "  • URL is temporary and will change if tunnel is restarted"
            ])

            return ToolResult(
                success=True,
                message="\n".join(msg_parts),
                data={
                    "url": public_url,
                    "port": port,
                    "method": method,
                    "description": description or f"Service on port {port}",
                    "status": "created",
                    "real_tunnel": True
                }
            )
        else:
            # Fallback to mock URL if cloudflared unavailable
            unique_id = str(uuid.uuid4())[:8]
            public_url = f"https://{port}-{unique_id}.apps.pime.ai"
            method = "mock"

            # Store the mapping
            self._port_mappings[port] = {
                "url": public_url,
                "unique_id": unique_id,
                "method": method,
                "description": description or f"Service on port {port}",
                "port": str(port)
            }

            warning = "⚠️  Cloudflared not available - using mock URL for testing"
            if not cloudflared_available:
                warning += "\n   Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"

            msg_parts = [
                f"⚠️  Exposed port {port} with MOCK URL (testing only)",
                f"🔗 Mock URL: {public_url}",
                "",
                warning,
                "",
                "Note: Ensure your application is bound to 0.0.0.0 to be accessible"
            ]

            if description:
                msg_parts.insert(1, f"📝 Service: {description}")

            return ToolResult(
                success=True,
                message="\n".join(msg_parts),
                data={
                    "url": public_url,
                    "port": port,
                    "unique_id": unique_id,
                    "method": method,
                    "description": description or f"Service on port {port}",
                    "status": "created",
                    "real_tunnel": False
                }
            )

    @tool(
        name="list_exposed_ports",
        description="List all currently exposed ports and their public URLs",
        parameters={},
        required=[]
    )
    async def list_exposed_ports(self) -> ToolResult:
        """List all exposed ports and their public URLs

        Returns:
            ToolResult containing list of exposed ports
        """
        if not self._port_mappings:
            return ToolResult(
                success=True,
                message="No ports are currently exposed",
                data={"exposed_ports": []}
            )

        exposed_list = [
            {
                "port": int(mapping["port"]) if isinstance(mapping["port"], str) else mapping["port"],
                "url": mapping["url"],
                "description": mapping["description"],
                "unique_id": mapping["unique_id"]
            }
            for mapping in self._port_mappings.values()
        ]

        message_lines = ["Currently exposed ports:"]
        for item in exposed_list:
            message_lines.append(
                f"  - Port {item['port']}: {item['url']}"
            )
            if item['description']:
                message_lines.append(f"    Description: {item['description']}")

        return ToolResult(
            success=True,
            message="\n".join(message_lines),
            data={"exposed_ports": exposed_list}
        )

    @tool(
        name="unexpose_port",
        description="Remove public URL exposure for a specified port and stop any running cloudflared tunnel",
        parameters={
            "port": {
                "type": "integer",
                "description": "Port number to stop exposing"
            }
        },
        required=["port"]
    )
    async def unexpose_port(self, port: int) -> ToolResult:
        """Remove public URL exposure for specified port

        Args:
            port: Port number to stop exposing

        Returns:
            ToolResult indicating success or failure
        """
        if port not in self._port_mappings:
            return ToolResult(
                success=False,
                message=f"Port {port} is not currently exposed",
                data=None
            )

        mapping = self._port_mappings.pop(port)

        # Terminate cloudflared process if it exists
        if "process" in mapping:
            try:
                process = mapping["process"]
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=5.0)
                tunnel_stopped = "✅ Cloudflared tunnel stopped"
            except asyncio.TimeoutError:
                process.kill()
                tunnel_stopped = "⚠️  Cloudflared tunnel forcefully killed"
            except Exception:
                tunnel_stopped = "⚠️  Failed to stop cloudflared tunnel (may still be running)"
        else:
            tunnel_stopped = None

        msg_parts = [f"✅ Removed exposure for port {port}"]

        if tunnel_stopped:
            msg_parts.append(tunnel_stopped)

        msg_parts.append(f"🔗 URL no longer accessible: {mapping['url']}")

        return ToolResult(
            success=True,
            message="\n".join(msg_parts),
            data={
                "port": port,
                "url": mapping["url"],
                "method": mapping.get("method", "mock"),
                "status": "removed"
            }
        )
