import main

FIELDS = list(main.CORE_FIELDS)


def test_same_seed_gives_the_same_users():
    first = main.generate(5, "en_GB", FIELDS, seed=42)
    second = main.generate(5, "en_GB", FIELDS, seed=42)
    assert first == second


def test_different_seeds_give_different_users():
    assert main.generate(5, "en_GB", FIELDS, seed=1) != main.generate(5, "en_GB", FIELDS, seed=2)


def test_without_a_seed_runs_differ():
    assert main.generate(5, "en_GB", FIELDS) != main.generate(5, "en_GB", FIELDS)


def test_seed_works_for_other_locales():
    assert main.generate(3, "fr_FR", FIELDS, seed=7) == main.generate(3, "fr_FR", FIELDS, seed=7)


def test_usernames_and_emails_are_unique():
    users = main.generate(200, "en_GB", ["username", "email"], seed=3)
    assert len({user["username"] for user in users}) == 200
    assert len({user["email"] for user in users}) == 200


def test_only_requested_fields_are_returned():
    users = main.generate(2, "en_GB", ["email", "ipv4"], seed=5)
    assert all(set(user) == {"email", "ipv4"} for user in users)


def test_handles_are_ascii():
    assert main.handle_part("Zoë-Ångström") == "zoeangstrom"
    assert main.handle_part("李") == "user"


def test_private_ips_stay_private():
    users = main.generate(20, "en_GB", ["ipv4"], private_ip=True, seed=9)
    assert all(user["ipv4"].startswith(("10.", "172.", "192.168.")) for user in users)
