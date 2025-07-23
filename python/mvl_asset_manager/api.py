import os
import json
import uuid
from collections import deque

class AssetManager:
    def __init__(self, db_file="V:\\tools\\asset-manager\\assets.json"):
        self.db_file = db_file

    def load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def save_db(self, db):
        with open(self.db_file, "w") as f:
            json.dump(db, f, indent=2)

    def add_asset(self, path, tags=None):
        db = self.load_db()
        asset_id = uuid.uuid4().hex[:6]
        asset = {
            "id": asset_id,
            "path": os.path.abspath(path),
            "tags": tags or [],
            "related": []
        }
        db.append(asset)
        self.save_db(db)
        return asset

    def tag_asset(self, asset_id, add=None, remove=None):
        db = self.load_db()
        for a in db:
            if a["id"] == asset_id:
                if add and add not in a["tags"]:
                    a["tags"].append(add)
                if remove and remove in a["tags"]:
                    a["tags"].remove(remove)
                self.save_db(db)
                return a
        raise ValueError("Asset not found.")

    def link_assets(self, from_id, to_id, unlink=False):
        db = self.load_db()

        from_asset = next((a for a in db if a["id"] == from_id), None)
        to_asset = next((a for a in db if a["id"] == to_id), None)

        if not from_asset or not to_asset:
            raise ValueError("One or both asset IDs not found.")

        # Ensure 'related' fields exist
        from_asset.setdefault("related", [])
        to_asset.setdefault("related", [])

        if unlink:
            # Remove links if present
            if to_id in from_asset["related"]:
                from_asset["related"].remove(to_id)
            if from_id in to_asset["related"]:
                to_asset["related"].remove(from_id)
            action = "Unlinked"
        else:
            # Add links only if not already present (prevent circular duplication)
            if to_id not in from_asset["related"]:
                from_asset["related"].append(to_id)
            if from_id not in to_asset["related"]:
                to_asset["related"].append(from_id)
            action = "Linked"

        self.save_db(db)
        return {"action": action, "from": from_asset["id"], "to": to_asset["id"]}

    def search_by_tag(self, tag):
        db = self.load_db()
        return [a for a in db if tag in a["tags"]]

    def get_asset_info(self, asset_id):
        db = self.load_db()
        asset = next((a for a in db if a["id"] == asset_id), None)
        if not asset:
            raise ValueError("Asset not found.")
        related = [a for a in db if a["id"] in asset.get("related", [])]
        return asset, related

    def bfs_walk_related_assets(self, root_id):
        db = self.load_db()
        queue = deque()
        visited = set()

        queue.append((root_id, 0))
        visited.add(root_id)
        results = []

        while queue:
            current_id, depth = queue.popleft()
            current = next((a for a in db if a["id"] == current_id), None)
            if not current:
                continue

            results.append((depth, current))

            for rel_id in current.get("related", []):
                if rel_id not in visited:
                    visited.add(rel_id)
                    queue.append((rel_id, depth + 1))

        return results
