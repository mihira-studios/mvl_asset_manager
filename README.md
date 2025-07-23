# Asset Manager CLI

A lightweight, command-line asset tracker for managing media pipeline assets such as `.exr`, `.mov`, and proxy files, with tagging and relationship support.

---

## Features

- Add and list assets with unique IDs
- Tag assets with metadata (e.g., `source`, `proxy`, `approved`)
- Query assets by tag
- Link related assets (e.g., `.exr` → `.mov` → `proxy`)
- Retrieve full information with related asset references

---

##  Installation

Clone the repository and install any dependencies:

```bash
git clone https://your.repo.url/here.git
cd asset-manager
pip install -r requirements.txt
```

*Ensure your `assets.json` DB path is correctly set in the script:*

```python
DB_FILE = "V:\\tools\\asset_manager\\assets.json"
```

> Replace with an appropriate path for your platform.

---

##  Usage

Run the CLI from the terminal:

```bash
python asset.py <command> [arguments]
```

---

## Commands

### `add`

Add a new asset to the database.

```bash
asset add /path/to/file.exr
```

---

### `list`

List all registered assets with their IDs and tags.

```bash
asset list
```

---

### `info`

View detailed info about an asset, including its related assets.

```bash
asset info <asset_id>
```

---

### `tag`

Add or remove tags on an asset.

```bash
asset tag <asset_id> --add source
asset tag <asset_id> --remove outdated
```

---

### `search`

Find all assets with a specific tag.

```bash
asset search approved
```

---

### `link`

Create a directional relationship between two assets. Useful for linking stages like `.exr` → `.mov` → `proxy`.

```bash
asset link <from_asset_id> <to_asset_id>
```

---

## 🧪 Example Workflow

```bash
# Add original .exr
asset add /project/shot01/image.exr   # id: abc123

# Add converted .mov
asset add /project/shot01/image.mov   # id: def456

# Add proxy
asset add /project/shot01/image_proxy.mov   # id: ghi789

# Tag them
asset tag abc123 --add source
asset tag def456 --add intermediate
asset tag ghi789 --add proxy

# Link the versions
asset link abc123 def456
asset link def456 ghi789

# Inspect the chain
asset info abc123
```

---

## Roadmap Ideas

- Tree or graph view for asset lineage
- Multi-tag queries with `AND/OR`
- UI frontend or web dashboard
- Asset versioning support
- Concurrency-safe file locking

---

## Logging

A logger is initialized using `mvl_core_pipeline.logger.Logger`, defaulting to DEBUG level. You can extend logging for deeper traceability or integrate with external log tools.

---

## 📁 Data Storage

Assets are stored in JSON format at the specified path. Sample entry:

```json
{
  "id": "abc123",
  "path": "/project/shot01/image.exr",
  "tags": ["source"],
  "related": ["def456"]
}
```

---
## 🧑‍💻 Contributors

Maintained by the MVL DEV Team.\
For support or issues, contact: [systems@mihira.studio.com](mailto\:systems@mihira.studio.com)
---

