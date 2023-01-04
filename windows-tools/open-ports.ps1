New-NetFirewallRule -DisplayName "25565-TCP" -Direction inbound -Profile Any -Action Allow -LocalPort 25565 -Protocol TCP
New-NetFirewallRule -DisplayName "25565-UDP" -Direction inbound -Profile Any -Action Allow -LocalPort 25565 -Protocol UDP

New-NetFirewallRule -DisplayName "25575-TCP" -Direction inbound -Profile Any -Action Allow -LocalPort 25565 -Protocol TCP
New-NetFirewallRule -DisplayName "25575-UDP" -Direction inbound -Profile Any -Action Allow -LocalPort 25565 -Protocol UDP