# 🎬 Asset Manager CLI

A lightweight, command-line asset tracker for managing media pipeline assets, and proxy files, with tagging and relationship support.

---

## Features

- Add and list assets with unique IDs
- Tag assets with metadata (e.g., `source`, `proxy`, `approved`)
- Query assets by tag
- Link related assets (e.g., `.exr` → `.mov` → `proxy`)
- Retrieve full asset info and visualize relationships
- Safeguard against circular dependency via traversal guards
- Optional DAG enforcement

---
```python
DB_FILE = "V:\\tools\\asset_manager\\assets.json"
```

---

## Usage

Run from MvlShell:
```bash
assetdb <command> [arguments]
```

---

## Commands

###  `add`
```bash
assetdb add /path/to/file.exr
```

---

### `list`
```bash
assetdb list
```

---

### `info`
```bash
assetdb info <asset_id>
```

---

### `tag`
```bash
assetdb tag <asset_id> --add source
assetdb tag <asset_id> --remove outdated
```

---

### `search`
```bash
assetdb search approved
```

---

### `link`
Create a one-way link (with optional DAG enforcement):

```bash
assetdb link <from_id> <to_id>
```

To unlink:
```bash
assetdb link <from_id> <to_id> --unlink
```

---

### `ingest`
Register and optionally tag and link in one step:

```bash
assetdb ingest /path/to/file.mov --tag proxy --link abc123
```

---

##  Example Workflow

```bash
# Add and tag files
assetdb add /shots/shot01/image.exr      # abc123
assetdb tag abc123 --add source

assetdb add /shots/shot01/image.mov      # def456
assetdb tag def456 --add intermediate

assetdb add /shots/shot01/image_proxy.mov  # ghi789
assetdb tag ghi789 --add proxy

# Link in processing order
assetdb link abc123 def456
assetdb link def456 ghi789

# View info with related assets
assetdb info abc123
```
---
## Logging

Configured via `mvl_core_pipeline.logger.Logger` (set to DEBUG). Extendable for CI/CD integrations or audit logging.

---

## Data Format

Sample JSON schema in `assets.json`:

```json
{
  "id": "abc123",
  "path": "/project/shot01/image.exr",
  "tags": ["source"],
  "related": ["def456"]
}
```

---

## 👥 Contributors

Maintained by the MVL DEV Team  
📧 [systems@mihira.studio](mailto:systems@mihira.studio)

---
