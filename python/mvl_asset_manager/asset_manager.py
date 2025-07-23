#!/usr/bin/env python3
import argparse
import json
import uuid
import os
import logging
from mvl_core_pipeline.logger import Logger


logger = Logger(name='movie_generator', repo_name='rez-make-dailies').get_logger()
logger.setLevel(logging.DEBUG)


DB_FILE = r"V:/tools/asset-manager/assets.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def cmd_add(args):
    db = load_db()
    asset_id = uuid.uuid4().hex[:6]
    db.append({
        "id": asset_id,
        "path": os.path.abspath(args.path),
        "tags": [],
        "related": [],
    })
    save_db(db)
    print(f"Added asset {asset_id}")

def cmd_list(args):
    db = load_db()
    for a in db:
        print(f"{a['id']}: {a['path']} (tags: {', '.join(a['tags'])})")

def cmd_info(args):
    db = load_db()
    for a in db:
        if a["id"] == args.id:
            related_assets = [rel for rel in db if rel["id"] in a.get("related", [])]
            print(json.dumps(a, indent=2))
            if related_assets:
                print("\nRelated assets:")
                for r in related_assets:
                    print(f"  {r['id']}: {r['path']} (tags: {', '.join(r['tags'])})")
            return
    print("Asset not found.")


def cmd_tag(args):
    db = load_db()
    for a in db:
        if a["id"] == args.id:
            if args.add:
                if args.add not in a["tags"]:
                    a["tags"].append(args.add)
            if args.remove:
                if args.remove in a["tags"]:
                    a["tags"].remove(args.remove)
            save_db(db)
            print("Tags updated.")
            return
    print("Asset not found.")

def cmd_search(args):
    db = load_db()
    results = [a for a in db if args.tag in a["tags"]]
    if not results:
        print(f"No assets found with tag '{args.tag}'.")
        return
    for a in results:
        print(f"{a['id']}: {a['path']} (tags: {', '.join(a['tags'])})")

def cmd_link(args):
    db = load_db()
    from_asset = next((a for a in db if a["id"] == args.from_id), None)
    to_asset = next((a for a in db if a["id"] == args.to_id), None)

    if not from_asset or not to_asset:
        print("One or both asset IDs not found.")
        return

    if args.to_id not in from_asset.get("related", []):
        from_asset.setdefault("related", []).append(args.to_id)
        save_db(db)
        print(f"Linked {args.from_id} → {args.to_id}")
    else:
        print("Link already exists.")



parser = argparse.ArgumentParser(prog="asset")
subparsers = parser.add_subparsers()

p_add = subparsers.add_parser("add")
p_add.add_argument("path")
p_add.set_defaults(func=cmd_add)

p_list = subparsers.add_parser("list")
p_list.set_defaults(func=cmd_list)

p_info = subparsers.add_parser("info")
p_info.add_argument("id")
p_info.set_defaults(func=cmd_info)

p_tag = subparsers.add_parser("tag")
p_tag.add_argument("id")
p_tag.add_argument("--add")
p_tag.add_argument("--remove")
p_tag.set_defaults(func=cmd_tag)

p_search = subparsers.add_parser("search")
p_search.add_argument("tag", help="Tag to search for")
p_search.set_defaults(func=cmd_search)

p_link = subparsers.add_parser("link")
p_link.add_argument("from_id", help="Source asset ID")
p_link.add_argument("to_id", help="Target (derived) asset ID")
p_link.set_defaults(func=cmd_link)



if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
