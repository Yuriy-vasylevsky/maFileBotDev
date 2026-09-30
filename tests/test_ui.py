from types import SimpleNamespace

from app.i18n import tr
from app.ui import admin_menu, code_availability_text, home_rows, persistent_menu, purchase_rows


def test_home_inline_menu_has_only_catalog_sections():
    rows = home_rows("ua")
    targets = [target for row in rows for _, target in row]
    assert "featured:0" in targets
    assert "catalog:0" in targets
    assert "cart:view" not in targets
    assert "purchases:0" not in targets
    assert "a:home" not in targets
def test_account_replaces_profile_actions_in_persistent_menu():
    markup = persistent_menu("ua", subscribed=True, loyalty_enabled=True)
    labels = [button.text for row in markup.keyboard for button in row]
    assert tr("account", "ua") in labels
    assert tr("language", "ua") not in labels
    assert tr("review", "ua") not in labels
    assert tr("loyalty", "ua") not in labels
    assert not any("розсил" in label.lower() for label in labels)


def test_admin_panel_stays_in_persistent_menu_for_admins():
    labels = [button.text for row in persistent_menu("ua", admin=True).keyboard for button in row]
    assert "⚙️ Адмін-панель" in labels


def test_admin_menu_has_steam_guard_action():
    labels = [button.text for row in admin_menu().keyboard for button in row]
    assert "🔑 Отримати код" in labels


def test_purchase_actions_include_steam_guard_when_available():
    order = SimpleNamespace(id="order-id")
    rows = purchase_rows(order, "ua", "support", True, 3)
    assert any(target == "code_request:order-id" for row in rows for _, target in row)


def test_expired_code_timer_removes_code_button():
    order = SimpleNamespace(id="order-id")
    rows = purchase_rows(
        order,
        "ua",
        "support",
        True,
        1,
        code_request_available=False,
        code_limit_exhausted=True,
    )

    assert not any(target.startswith("code_request:") for row in rows for _, target in row)


def test_code_availability_explains_single_code_and_timed_multiple_codes():
    single = SimpleNamespace(steam_authenticator_id=1, code_limit=1, code_cooldown_hours=0)
    timed = SimpleNamespace(steam_authenticator_id=1, code_limit=2, code_cooldown_hours=48)

    assert "180 днів" in code_availability_text(single, "ua")
    timed_text = code_availability_text(timed, "ua")
    assert "180 днів" in timed_text
    assert "48 год." in timed_text
    assert "Решту кодів" in timed_text


def test_purchase_code_confirmation_preserves_purchases_page():
    order = SimpleNamespace(id="order-id")
    rows = purchase_rows(order, "ua", "support", True, 3, return_target="purchases:2")
    assert any(target == "code_request:order-id:2" for row in rows for _, target in row)


def test_exhausted_code_limit_shows_support_button():
    order = SimpleNamespace(id="order-id")
    rows = purchase_rows(order, "ua", "@support", True, 0, code_limit_exhausted=True)

    assert any(target == "https://t.me/support" for row in rows for _, target in row)
    assert not any(target.startswith("code_request:") for row in rows for _, target in row)


def test_alternative_activation_guide_comes_from_order_snapshot():
    order = SimpleNamespace(id="order-id", activation_type_snapshot="alternative")
    rows = purchase_rows(order, "ua", "support")

    assert rows[0][0][1] == "alternative_activation_guide:order-id"
