param (
    [string]$Port,
    [string]$Endpoint = "core",
    [int]$MaxRetries = 10
)

$Url = "http://localhost:${Port}/${Endpoint}"
$Success = $false

for ($i = 1; $i -le $MaxRetries; $i++) {
    try {
        $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
        if ($Response.StatusCode -eq 200) {
            Write-Host "Success! Response from $Url is 200 OK."
            $Success = $true
            break
        }
    } catch {
        Write-Host "Waiting for $Url... ($i/$MaxRetries)"
        Start-Sleep -Seconds 3
    }
}

if (-not $Success) {
    Write-Error "Health check failed for $Url after $MaxRetries attempts."
    exit 1
}