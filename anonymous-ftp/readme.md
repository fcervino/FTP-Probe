# anon-ftp

Checks if the target FTP server is vulnerable to anonymous login

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
    "Is vulnerable to anonymous login": true
  }
}
```

An example of a safe target:

```json5
{
  "status": true,
  "data": {
    "Is vulnerable to anonymous login": false
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