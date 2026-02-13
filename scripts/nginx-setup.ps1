'''
$PSScriptRoot : directory under scripts
'''
Write-Host "Starting Infrastructure Setup..."

# 1. Create Network
# Ensuring the internal communication channel exists.
if (-not (docker network ls -q -f name=test-net)) {
    docker network create test-net
    Write-Host "Network 'test-net' created."
}

# 2. Check/Build Image
# We need the production image to launch the initial app.
if (-not (docker images -q my-app:prod)) {
    Write-Host "Image 'my-app:prod' not found. Building it now..."
    docker build --target production -t my-app:prod -f app/Dockerfile .
}

# 3. Determine Active App (Blue vs Green)
$ConfPath = "$PSScriptRoot\..\nginx\myapp.conf" # Adjust path if needed
$TargetContainer = "app-blue"
$TargetPort = "5001"

if (-not (Test-Path $ConfPath)) {
    Write-Host "Config file not found. Creating a default one (Blue)..."
    Copy-Item "$PSScriptRoot\..\nginx\templates\blue.conf" -Destination $ConfPath
}

$ConfContent = Get-Content $ConfPath -Raw
if ($ConfContent -match "app-green") {
    Write-Host "Config points to GREEN."
    $TargetContainer = "app-green"
    $TargetPort = "5002"
}

# 4. Run the App Container (Graceful)
# Nginx won't start if this container is missing.
if (docker ps -a -q -f name=$TargetContainer) {
    Write-Host "Stopping existing $TargetContainer gracefully..."
    docker stop $TargetContainer
    docker rm $TargetContainer
}

Write-Host "Starting '$TargetContainer'..."
docker run -d --name $TargetContainer `
    --network test-net `
    -p "${TargetPort}:5000" `
    -e Page_Title="Initial App ($TargetContainer)" `
    --restart always `
    my-app:prod

# 5. Wait for App to be Ready
& "$PSScriptRoot\check-health.ps1" -Port $TargetPort

# 6. Handle Nginx (Graceful Shutdown with SIGQUIT)
$NginxName = "nginx-proxy"
if (docker ps -q -f name=$NginxName) { 
    Write-Host "Gracefully shutting down existing '$NginxName'..."
    docker kill -s SIGQUIT $NginxName
    
    $Timeout = 20
    $Count = 0
    while ((docker ps -q -f name=$NginxName) -and ($Count -lt $Timeout)) {
        Start-Sleep -Seconds 1
        $Count++
    }
    docker rm -f $NginxName | Out-Null
} elseif (docker ps -a -q -f name=$NginxName) {
    docker rm $NginxName | Out-Null
}

# 7. Start Nginx Proxy
Write-Host "Starting 'nginx-proxy' with Template..."

# Nginx will receive TARGETContainer by -e option on docker run 
docker run -d --name $NginxName `
    --network test-net `
    -p 80:80 `
    -p 5004:5000 `
    -e TARGET="$TargetContainer" `
    --restart always `
    -v "${PSScriptRoot}\..\nginx\myapp.conf.template:/etc/nginx/templates/default.conf.template" `
    nginx:alpine

# 8. Final Verification
& "$PSScriptRoot\check-health.ps1" -Port 5004 -Endpoint "status"

Write-Host "------------------------------------------------"
Write-Host "Infrastructure Setup Complete!"
Write-Host "------------------------------------------------"