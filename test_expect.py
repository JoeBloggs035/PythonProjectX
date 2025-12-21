# Тест проверки заполнения формы
#
# открыть https://demo.playwright.dev/todomvc/#/
# проверить что открыт корректный url
# найти поле ввода задачи
# проверить что оно пустое
# ввести задачу номер один
# ввести задачу номер два
# проверить что количество задач в списке равно двум
# отметить одну задачу выполненной
# проверить что эта задача отмечена выполненной
import time
from playwright.sync_api import expect


# pytest --headed -vsk 'test_expect'
def test_expect(page):
    page.goto("https://demo.playwright.dev/todomvc/#/")
    # page.pause() # останавливает выполнение теста и открывает окно TestInspector (только в --headed)
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")
    input_field = page.locator("input.new-todo")
    expect(input_field).to_be_empty()
    input_field.fill("task 1")
    input_field.press("Enter")
    input_field.fill("task 2")
    input_field.press("Enter")
    time.sleep(3)
    todo_items = page.get_by_test_id("todo-item")
    expect(todo_items).to_have_count(2)
    toggle2 = page.locator("input.toggle").locator("nth=1")
    toggle2.check()
    time.sleep(3)
    expect(toggle2).to_be_checked()
