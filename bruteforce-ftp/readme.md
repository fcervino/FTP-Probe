# anon-ftp

Checks if the target FTP server has vulnerable valid credentials

The tool has been modified to emit json, exit codes have changed as well.

## Input

```json5
{
  "config": {
    "host": "172.20.28.159"
  }
}
```

## Output

The output is `True` iff the target is safe.

An example of a vulnerable target:

```json5
{
  "status": false,
  "data": {
    "Has vulnerable credentials": true
  }
}
```

An example of a safe target:

```json5
{
  "status": true,
  "data": {
    "Has vulnerable credentials": false
  }
}
```

An example of target with fail2ban implemented:

```json5
{
  "status": false,
  "data": {
    "Has fail2ban implemented": true
  }
}
```

When an error occurs:

```json5
{
  "status": false,
  "data": {
    "ERROR": "Check if the host is up and contact Moon Cloud admin"
  }
}
```