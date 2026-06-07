import csv
import json
import os
import random
import argparse
import sys
from faker import Faker

CORE_FIELDS = [
    "first_name",
    "last_name",
    "username",
    "email",
    "password",
    "company",
    "ipv4",
    "user_agent",
]

OPTIONAL_FIELDS = {
    "address":  ["address", "city", "country", "postcode"],
    "dob":      ["birthday"],
    "phone":    ["phone"],
    "job":      ["job"],
}

DEFAULT_COUNT  = 20
DEFAULT_LOCALE = "en_GB"
DEFAULT_FORMAT = "csv"
DEFAULT_OUTPUT = "users"


def make_user(fake: Faker, private_ip: bool = False) -> dict:
    first = fake.first_name()
    last  = fake.last_name()
    return {
        "first_name":  first,
        "last_name":   last,
        "username":    f"{first.lower()}{last.lower()}{random.randint(1, 999)}",
        "email":       f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@{fake.free_email_domain()}",
        "password":    fake.password(length=16, special_chars=True, digits=True, upper_case=True),
        "birthday":    fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
        "phone":       fake.phone_number(),
        "address":     fake.street_address().replace("\n", ", "),
        "city":        fake.city(),
        "country":     fake.country(),
        "postcode":    fake.postcode(),
        "job":         fake.job(),
        "company":     fake.company(),
        "ipv4":        fake.ipv4_private() if private_ip else fake.ipv4(),
        "user_agent":  fake.user_agent(),
    }


def build_fields(args) -> list:
    """Assemble the ordered list of fields based on CLI flags."""
    fields = list(CORE_FIELDS)
    if args.include_address:
        fields.extend(OPTIONAL_FIELDS["address"])
    if args.include_dob:
        fields.extend(OPTIONAL_FIELDS["dob"])
    if args.include_phone:
        fields.extend(OPTIONAL_FIELDS["phone"])
    if args.include_job:
        fields.extend(OPTIONAL_FIELDS["job"])
    if args.fields:
        requested = [f.strip() for f in args.fields.split(",")]
        all_known = list(CORE_FIELDS) + [f for v in OPTIONAL_FIELDS.values() for f in v]
        invalid = [f for f in requested if f not in all_known]
        if invalid:
            print(f"  Unknown fields: {', '.join(invalid)}")
            print(f"  Available: {', '.join(all_known)}")
            sys.exit(1)
        fields = requested
    return fields


def generate(count: int, locale: str, fields: list, private_ip: bool = False) -> list:
    try:
        fake = Faker(locale)
    except AttributeError:
        print(f"  Warning: locale '{locale}' not found, falling back to en_GB.")
        fake = Faker("en_GB")
    Faker.seed()
    users = []
    seen_usernames = set()
    seen_emails = set()
    for _ in range(count):
        row = make_user(fake, private_ip=private_ip)
        while row["username"] in seen_usernames or row["email"] in seen_emails:
            row = make_user(fake, private_ip=private_ip)
        seen_usernames.add(row["username"])
        seen_emails.add(row["email"])
        users.append({f: row[f] for f in fields})
    return users


def save_csv(users: list, path: str, append: bool):
    file_exists = os.path.isfile(path)
    mode = "a" if append else "w"
    write_header = not (append and file_exists)
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=users[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(users)


def save_json(users: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def print_table(users: list):
    if not users:
        return
    keys = list(users[0].keys())
    col_w = {k: max(len(k), max(len(str(u[k])) for u in users)) for k in keys}
    header = "  ".join(k.ljust(col_w[k]) for k in keys)
    print("\n" + header)
    print("-" * len(header))
    for u in users:
        print("  ".join(str(u[k]).ljust(col_w[k]) for k in keys))


def parse_args():
    all_fields = list(CORE_FIELDS) + [f for v in OPTIONAL_FIELDS.values() for f in v]
    p = argparse.ArgumentParser(
        description="Generate fake user credential data for testing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available fields: {', '.join(all_fields)}",
    )
    p.add_argument("-n", "--count",   type=int, default=DEFAULT_COUNT,
                   help=f"Number of records to generate (default: {DEFAULT_COUNT})")
    p.add_argument("-l", "--locale",  type=str, default=DEFAULT_LOCALE,
                   help=f"Faker locale, e.g. en_GB, fr_FR, de_DE (default: {DEFAULT_LOCALE})")
    p.add_argument("-f", "--format",  type=str, default=DEFAULT_FORMAT, choices=["csv", "json"],
                   help="Output format (default: csv)")
    p.add_argument("-o", "--output",  type=str, default=None,
                   help="Output filename without extension (default: users)")
    p.add_argument("--fields",        type=str, default=None,
                   help=f"Comma-separated list of specific fields to include. Overrides --include-* flags.")
    p.add_argument("--no-save",       action="store_true",
                   help="Print to terminal only; do not save a file")
    p.add_argument("--append",        action="store_true",
                   help="Append to existing output file instead of overwriting; skips header if file exists")
    p.add_argument("--private-ip",    action="store_true",
                   help="Generate private/LAN IP addresses (10.x, 172.16.x, 192.168.x) instead of public ones")
    p.add_argument("--include-address", action="store_true",
                   help="Include street address, city, country, postcode")
    p.add_argument("--include-dob",     action="store_true",
                   help="Include date of birth (birthday)")
    p.add_argument("--include-phone",   action="store_true",
                   help="Include phone number")
    p.add_argument("--include-job",     action="store_true",
                   help="Include job title")
    args = p.parse_args()
    if args.count <= 0:
        p.error("--count must be a positive integer")
    return args


def main():
    args = parse_args()
    fields = build_fields(args)

    ip_mode = "private" if args.private_ip else "public"
    print(f"  Generating {args.count} fake user(s) [{args.locale}] [IPv4: {ip_mode}] ...")
    users = generate(args.count, args.locale, fields, private_ip=args.private_ip)

    print_table(users)

    if not args.no_save:
        out_name = args.output or DEFAULT_OUTPUT
        ext  = args.format
        path = f"{out_name}.{ext}"
        if ext == "csv":
            save_csv(users, path, args.append)
        else:
            save_json(users, path)
        action = "Appended" if args.append else "Saved"
        print(f"\n  {action} {args.count} record(s) to: {path}")


if __name__ == "__main__":
    main()
