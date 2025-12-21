import time


def test_built_in_locators(page):
    page.goto("https://zimaev.github.io/text_input/")
    page.get_by_label("Email address").fill("niqasebe@example.com")
    # time.sleep(1)
    page.get_by_title("username").type("Joseph")
    # time.sleep(1)
    page.get_by_placeholder("password").fill("big_secret")
    # time.sleep(1)
    page.get_by_role("checkbox").click()
    # time.sleep(2)


def test_or(page):
    page.goto("https://zimaev.github.io/text_input/")
    selector = (
        page.locator("input").locator("nth=1").or_(page.locator("text"))
    )  # метод or_
    selector.type(
        "Hello Stepik Hello Stepik Hello Stepik Hellooooooooooooooo Stepik!  <------------- .type()"
    )
    # time.sleep(1)
    selector = (
        page.locator("input").locator("nth=0").or_(page.locator("text"))
    )  # метод or_
    selector.fill(
        "Hello Stepik Hello Stepik Hello Stepik Hello Stepik!!!!!!!!!!!!!!!!!!!!!!  <------------- .fill()"
    )
    # time.sleep(2)


def test_locator_and(page):
    page.goto("https://zimaev.github.io/locatorand/")
    selector = page.get_by_role("button", name="Sing up").and_(
        page.get_by_title("Sing up today")
    )
    selector.click()
    # time.sleep(2)


def test_chain(page):
    page.goto("https://zimaev.github.io/navbar/")
    page.locator(
        "#navbarNavDropdown >> li:has-text('Company')"
    ).click()  # the chain of locators is here
    # time.sleep(1)
    page.locator("a:has-text('Contact us')").click()
    # time.sleep(2)


def test_filter(page):
    page.goto("https://zimaev.github.io/filter/")
    row_locator = page.locator("tr")
    how_many_buttons = row_locator.filter(has_not=page.get_by_role("button")).count()
    if how_many_buttons > 1:
        print("\nthere are", how_many_buttons, "buttons")
    else:
        print("\nthere is", how_many_buttons, "button")
    row_locator.filter(has_not_text="helicopter")
    row_locator.filter(has_text="QA").filter(
        has=page.get_by_role("button", name="Edit")
    ).click()
    # time.sleep(2)


# необходимо сделать клик по всем элементам чекбокс
class TestCheckboxes:
    def test_many_checkboxes(self, page):
        page.goto("https://zimaev.github.io/checks-radios/")
        checkbox = page.locator("input")  # будет соответствовать нескольким элементам
        for i in range(
            checkbox.count()
        ):  # чтобы узнать количество элементов, соответствующих указанному
            # селектору - используйте метод count()
            checkbox.nth(
                i
            ).click()  # чтобы взаимодействовать с конкретным элементом из списка,
            # используйте метод nth() с указанием индекса нужного вам элемента,
            # это сработает и без count() если вместо i подставить индекс нужного элемента
            # locator.first, locator.last вернут первый и последний элемент из списка.
        # time.sleep(2)

    # Начиная с версии playwright 1.29 появился метод locator.all()
    # возвращает массив локаторов указывающих на соответствующие элементы
    def test_many_checkboxes2(self, page):
        page.goto("https://zimaev.github.io/checks-radios/")
        checkboxes = page.locator("input")
        for checkbox in checkboxes.all():
            checkbox.check()
        # time.sleep(2)


# 10. Выпадающий список создается с помощью тега <select>, который представляет собой
# элемент управления интерфейса, в виде раскрывающегося списка. Каждый пункт выпадающего
# списка задается с помощью тега <option>

# Метод select_option() проверяет, что целевой элемент является тегом <select>
# В качестве аргумента данного метода, передается один из трех атрибутов, который
# определяет стратегию поиска пункта в выпадающем списке (value, index, label):


def test_select(page):
    page.goto("https://zimaev.github.io/select/")
    page.select_option(
        "#floatingSelect", value="3"
    )  # - для выбора по значению атрибута value
    # time.sleep(1)
    page.select_option("#floatingSelect", index=1)  # - опции для выбора по индексу
    # time.sleep(1)
    page.select_option(
        "#floatingSelect", label="Нашел и завел bug"
    )  # - выбор по текстовому значению
    # time.sleep(1)
    page.select_option(
        "#floatingSelect", "3"
    )  # - в кавычках без явного указания стратегии поиска
    # time.sleep(1)
    page.select_option(
        "#floatingSelect", "Нашел и завел bug"
    )  # - в кавычках без явного указания стратегии поиска
    # time.sleep(1)
    page.select_option(
        "#skills", value=["playwright", "python"]
    )  # либо массив опций при возможности множественного выбора
    # time.sleep(2)


def test_drag_and_drop(page):
    page.goto("https://zimaev.github.io/draganddrop/")
    # time.sleep(1)
    page.drag_and_drop(
        "#drag", "#drop"
    )  # в качестве аргументов селекторы source (элемента для перетаскивания)
    # и target(элемента на который следует перетащить)
    # time.sleep(1)


def test_dialogs(page):

    page.goto("https://zimaev.github.io/dialog/")

    # time.sleep(1)
    # выведем в терминал тип диалогового окна и сообщение, содержащееся в нём, после чего акцептируем
    # документация по диалоговым окнам в playwright здесь: https://playwright.dev/python/docs/api/class-dialog
    page.once(
        "dialog",
        lambda dialog: [print("\n", dialog.type, ":", dialog.message), dialog.accept()],
    )  # так Alert будет принят (нажата кнопка OK) и закроется
    page.get_by_text("Диалог Alert").click()

    # time.sleep(1)
    # page.once("dialog", lambda dialog: dialog.dismiss()) # так Confirmation будет отклонено (нажат Cancel) и закрыто
    page.get_by_text(
        "Диалог Confirmation"
    ).click()  # хотя Playwright и так его автоматически закроет через dismiss

    # time.sleep(1)
    # так Prompt останется открытым 3 секунды, затем принят (кнопка ОК) и закрыт
    page.once(
        "dialog", lambda dialog: [time.sleep(3), dialog.accept("2345")]
    )  # accept ещё и принимает строки в качестве аргумента
    page.get_by_text("Диалог Prompt").click()
    # time.sleep(3)


class TestUploadFile:
    def test_upload_file(self, page):
        page.goto("https://zimaev.github.io/upload/")
        # time.sleep(1)
        page.set_input_files("#formFile", "upload_test.txt")
        # time.sleep(1)
        page.locator("#file-submit").click()
        # time.sleep(2)

    def test_select_multiple(self, page):
        # по-моему этот тест ничего не постит, имя файла так и не появляется в строке...
        page.goto("https://zimaev.github.io/upload/")
        # time.sleep(1)
        page.on(
            "filechooser",
            lambda file_chooser: file_chooser.set_files("upload_test2.txt"),
        )
        # time.sleep(1)
        page.locator("#formFile").click()
        # time.sleep(2)

    def test_upload_file3(self, page):
        page.goto("https://zimaev.github.io/upload/")
        # time.sleep(1)
        with page.expect_file_chooser() as fc_info:
            page.locator("#formFile").click()
        # time.sleep(1)
        file_chooser = fc_info.value
        file_chooser.set_files("upload_test.txt")
        # time.sleep(2)


def test_download(page):

    page.goto(
        "https://demoqa.com/upload-download", wait_until="commit"
    )  # или wait_until = 'domcontentloaded'

    # Start waiting for the download
    with page.expect_download() as download_info:  # Контекстный менеджер with гарантирует, что ожидание начнется до клика
        # Perform the action that initiates download
        page.locator(
            "#downloadButton"
        ).click()  # Внутри блока with выполняется клик по кнопке скачивания
    download = download_info.value  # содержит путь и имя скачиваемого файла

    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as("./download_data/" + download.suggested_filename)


def test_inner_text_content(page):
    page.goto("https://zimaev.github.io/table/")
    element = page.locator('tr:has-text("Thornton")')
    print(
        "inner_text():", element.inner_text(), "\n"
    )  # умеет считывать стили и не возвращает содержимое скрытых элементов, тогда как textContent этого не делает
    print(
        "text_content():", element.text_content(), "\n"
    )  # получает содержимое всех элементов, включая <script> и <style>, тогда как innerText этого не делает.
    print(
        "inner_html():", element.inner_html(), "\n"
    )  # кроме текста, можно получить HTML-код элемента

    row = page.locator("tr")
    print("all_inner_texts():", row.all_inner_texts(), "\n")
    print("all_text_contexts():", row.all_text_contents())


def test_screenshots(page):
    page.goto("https://zimaev.github.io/table/")
    page.screenshot(path="./screenshots/screenshot.png")
    page.screenshot(path="./screenshots/screenshot1.png", full_page=True)
    page.locator(".table").screenshot(path="./screenshots/screenshot2.png")
    page.screenshot(path="./screenshots/screenshot3.jpeg", type="jpeg")
    page.screenshot(path="./screenshots/screenshot4.jpeg", type="jpeg", quality=50)
    page.screenshot(
        path="./screenshots/screenshot5.png",
        clip={"x": 50, "y": 0, "width": 400, "height": 300},
    )
    page.screenshot(
        path="./screenshots/screenshot6.png", omit_background=True
    )  # прозрачный фон
    page.screenshot(path="./screenshots/screenshot7.png", timeout=10000)


def test_new_tab(page):
    page.goto("https://zimaev.github.io/tabs/")
    # Метод page.context.expect_page()  ожидает открытия новой вкладки.
    # Переменная tab - это класс EventInfo, возвращаемый менеджером контекста with.
    # Мы можем получить доступ к классу с помощью свойства value.
    with page.context.expect_page() as tab:
        page.get_by_text("Переход к Dashboard").click()

    new_tab = tab.value
    assert new_tab.url == "https://zimaev.github.io/tabs/dashboard/index.html?"
    sign_out = new_tab.locator(".nav-link", has_text="Sign out")
    assert sign_out.is_visible()
