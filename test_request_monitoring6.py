import allure
import pytest
from playwright.sync_api import expect


@allure.description("Описание теста")
def test_listen_network(page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto("https://osinit.ru/")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skip(reason="данные не подменяются, ожидаемой ошибки не происходит, сайт изменился, указанных селекторов больше не существует")
def test_network(page):
    page.route(
        "**/api/register/4",
        lambda route: route.continue_(
            post_data='{"email": "joseph.bloggs@reqres.in","password": "secret"}'
        ),
    )
    page.goto("https://reqres.in/")
    page.get_by_text(" Register - successful ").click()
    response = page.locator('[data-key="output-response"]')
    expect(response).to_contain_text("error")
    # time.sleep(10)


def test_mynetwork(page):
    page.route(
        "**/v2/user/JoeBloggs035",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 8249734974133026000, "username": "JoeBloggs035", "firstName": "Joseph", "lastName": "Bloggs", "email": "joseph.bloggs@reqres.in", "password": "corset", "phone": "Terrorists Win", "userStatus": 0}',
        ),
    )
    page.goto("https://petstore.swagger.io/")
    page.locator(
        "div#operations-user-getUserByName button.opblock-summary-control"
    ).click()
    page.locator("div#operations-user-getUserByName button.btn.try-out__btn").click()
    page.locator("div#operations-user-getUserByName input").fill("JoeBloggs035")
    page.locator("div#operations-user-getUserByName button.btn.execute").click()
    response = page.locator(
        "div#operations-user-getUserByName pre.microlight code.language-json"
    ).locator("nth=0")
    # time.sleep(10)
    expect(response).to_contain_text("Terrorists Win")


def test_mynetwork2(page):
    # Перехватываем запрос и подменяем ответ
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 8249734974133026000, "username": "JoeBloggs035", "firstName": "Joseph", "lastName": "Bloggs", "email": "joseph.bloggs@reqres.in", "password": "corset", "phone": "Terrorists Win2", "userStatus": 0}',
        )

    page.route("**/v2/user/JoeBloggs035", handle_route)

    page.goto("https://petstore.swagger.io/")
    page.locator(
        "div#operations-user-getUserByName button.opblock-summary-control"
    ).click()
    page.locator("div#operations-user-getUserByName button.btn.try-out__btn").click()
    page.locator('div#operations-user-getUserByName input[type="text"]').fill(
        "JoeBloggs035"
    )
    page.locator("div#operations-user-getUserByName button.btn.execute").click()
    # time.sleep(10)
    response = page.locator(
        "div#operations-user-getUserByName pre.microlight code.language-json"
    ).locator("nth=0")
    expect(response).to_contain_text("Terrorists Win2")


# @pytest.mark.xfail(reason="https://demo.realworld.io/ not load")
def test_mock_tags(page):
    page.route("**/api/tags", lambda route: route.fulfill(path="data.json"))
    page.goto("https://demo.realworld.io/")


@pytest.mark.xfail(reason="https://demo.realworld.io/ not load")
def test_intercepted(page):
    def handle_route(route):
        response = route.fetch()
        json = response.json()
        json["tags"] = ["open", "solutions"]
        route.fulfill(json=json)

    page.route("**/api/tags", handle_route)

    page.goto("https://demo.realworld.io/")
    sidebar = page.locator("css=div.sidebar")
    expect(sidebar.get_by_role("link")).to_contain_text(["open", "solutions"])


#  playwright open --save-har=example.har --save-har-glob="**/api/**" https://reqres.in
@pytest.mark.skip(
    reason="example.har не содержит нужных сведений, сайт изменился указанных селекторов больше не существует"
)
def test_replace_from_har(page):
    page.goto("https://reqres.in/")
    page.route_from_har("example.har")
    users_single = page.locator('li[data-id="users-single"]')
    users_single.click()
    response = page.locator('[data-key="output-response"]')
    expect(response).to_contain_text("Terrorists Win")


# playwright open --save-har=example3.har --save-har-glob="**/v2/user/**" https://petstore.swagger.io/
# изменяем в example3.har поля "response":{"status": 200, "content":{"text": "{\"data\":{\"id\":8249734974133026000, \"username\": \"JoeBloggs035\", \"firstName\": \"Joseph\", \"lastName\": \"Bloggs\",\"email\":\"joseph.bloggs035@gmail.com\",\"password\": \"corset\", \"phone\": \"Terrorists Win\", \"userStatus\": 0}}"}
def test_replace_from_myhar(page):
    page.goto("https://petstore.swagger.io/")
    page.route_from_har("example3.har")
    page.locator(
        "div#operations-user-getUserByName button.opblock-summary-control"
    ).click()
    page.locator("div#operations-user-getUserByName button.btn.try-out__btn").click()
    page.locator('div#operations-user-getUserByName input[type="text"]').fill(
        "JoeBloggs035"
    )
    page.locator("div#operations-user-getUserByName button.btn.execute").click()
    # time.sleep(10)
    response = page.locator(
        "div#operations-user-getUserByName pre.microlight code.language-json"
    ).locator("nth=0")
    expect(response).to_contain_text("Terrorists Win")


def test_inventory(page):
    response = page.request.get("https://petstore.swagger.io/v2/store/inventory")
    print(response.status)
    print(response.json())


def test_add_user(page):
    data = [
        {
            "id": 97444444,
            "username": "GGGGGGGGGGGGGGGGG",
            "firstName": "fff",
            "lastName": "ggg",
            "email": "bbb",
            "password": "tt",
            "phone": "333",
            "userStatus": 0,
        }
    ]
    header = {"accept": "application/json", "content-Type": "application/json"}
    response = page.request.post(
        "https://petstore.swagger.io/v2/user/createWithArray", data=data, headers=header
    )
    print(response.status)
    print(response.json())
    # time.sleep(7)
