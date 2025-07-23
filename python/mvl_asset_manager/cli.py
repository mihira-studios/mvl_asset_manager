#!/usr/bin/env python3
import argparse
import json
from mvl_asset_manager.api import AssetManager

asm = AssetManager()

def cmd_add(args):
    asset = asm.add_asset(args.path)
    print(f"Added asset {asset['id']} at {asset['path']}")

def cmd_list(args):
    db = asm.load_db()
    for a in db:
        print(f"{a['id']}: {a['path']} (tags: {', '.join(a['tags'])})")

def cmd_info(args):
    try:
        asset, related = asm.get_asset_info(args.id)
        print(json.dumps(asset, indent=2))
        if related:
            print("\nRelated assets:")
            for r in related:
                print(f"  {r['id']}: {r['path']} (tags: {', '.join(r['tags'])})")
    except ValueError as e:
        print(str(e))

def cmd_tag(args):
    try:
        asset = asm.tag_asset(args.id, add=args.add, remove=args.remove)
        print(f"Updated tags: {asset['tags']}")
    except ValueError as e:
        print(str(e))

def cmd_link(args):
    try:
        result = asm.link_assets(args.from_id, args.to_id, unlink=args.unlink)
        print(f"{result['action']} {result['from']} ↔ {result['to']}")
    except ValueError as e:
        print(str(e))


def cmd_search(args):
    results = asm.search_by_tag(args.tag)
    if not results:
        print(f"No assets found with tag '{args.tag}'")
    for a in results:
        print(f"{a['id']}: {a['path']} (tags: {', '.join(a['tags'])})")

def cmd_ingest(args):
    asset = asm.add_asset(args.path, tags=[args.tag] if args.tag else [])
    if args.link:
        try:
            asm.link_assets(args.link, asset["id"])
            print(f"Linked {args.link} → {asset['id']}")
        except ValueError as e:
            print(str(e))
    print("Ingested asset:")
    print(json.dumps(asset, indent=2))

def main():
    parser = argparse.ArgumentParser(prog="asset")
    subparsers = parser.add_subparsers()

    # add
    p_add = subparsers.add_parser("add")
    p_add.add_argument("path")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = subparsers.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    # info
    p_info = subparsers.add_parser("info")
    p_info.add_argument("id")
    p_info.set_defaults(func=cmd_info)

    # tag
    p_tag = subparsers.add_parser("tag")
    p_tag.add_argument("id")
    p_tag.add_argument("--add")
    p_tag.add_argument("--remove")
    p_tag.set_defaults(func=cmd_tag)

    # link
    p_link = subparsers.add_parser("link")
    p_link.add_argument("from_id")
    p_link.add_argument("to_id")
    p_link.add_argument("--unlink", action="store_true", help="Unlink the two assets")
    p_link.set_defaults(func=cmd_link)

    # search
    p_search = subparsers.add_parser("search")
    p_search.add_argument("tag")
    p_search.set_defaults(func=cmd_search)

    # ingest
    p_ingest = subparsers.add_parser("ingest")
    p_ingest.add_argument("path")
    p_ingest.add_argument("--tag", help="Tag to apply to the asset")
    p_ingest.add_argument("--link", help="Parent asset ID to link from")
    p_ingest.set_defaults(func=cmd_ingest)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
