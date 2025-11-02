import requests
import sys
import time

# Адрес твоего сервера Flask
BASE_URL = "http://127.0.0.1:5000"
ENDPOINT = "/metrics"
URL = BASE_URL + ENDPOINT
TIMEOUT = 5  #sec waiting time

results = []


def log(message):
    print(message)
    sys.stdout.flush()


def check(condition, name, success_msg="OK", fail_msg="Ошибка"):
    if condition:
        results.append((name, True))
        log(f"[✅ OK]  {name} — {success_msg}")
    else:
        results.append((name, False))
        log(f"[❌ FAIL] {name} — {fail_msg}")


def req_get():
    try:
        r = requests.get(URL, timeout=TIMEOUT)
        return r.status_code, r.json()
    except Exception as e:
        return 0, str(e)


def req_delete():
    try:
        r = requests.delete(URL, timeout=TIMEOUT)
        return r.status_code, r.json()
    except Exception as e:
        return 0, str(e)


def req_post(json_body=None):
    try:
        r = requests.post(URL, json=json_body, timeout=TIMEOUT)
        body = r.json() if r.content else None
        return r.status_code, body
    except Exception as e:
        return 0, str(e)


def run_tests():
    log("=== ТЕСТ API НАЧАТ ===")
    log(f"Проверяем адрес: {URL}\n")

    # 1️⃣ Очистка данных
    log("1️⃣ DELETE — очистка данных")
    status, body = req_delete()
    check(status == 200, "DELETE (очистка)", success_msg=f"код {status}", fail_msg=f"{status} / {body}")

    # 2️⃣ Проверка GET — должен вернуть пустой список
    log("\n2️⃣ GET — проверяем, что данных нет")
    status, body = req_get()
    cond = (status == 200) and isinstance(body, list)
    check(cond, "GET (пустой список)", success_msg=f"код {status}, {len(body)} элементов", fail_msg=f"{status} / {body}")

    # 3️⃣ POST без тела
    log("\n3️⃣ POST без тела — сервер не должен упасть")
    status, body = req_post()
    cond = (status == 200)
    check(cond, "POST без тела", success_msg=f"код {status}", fail_msg=f"{status} / {body}")

    # 4️⃣ POST с неверными логином/паролем
    log("\n4️⃣ POST с неправильными логином/паролем")
    status, body = req_post({"login": "user", "password": "bad"})
    cond = (status == 200)
    has_unauth = isinstance(body, list) and "Unauthorized" in str(body)
    check(cond and has_unauth, "POST (неверные данные)", success_msg=f"код {status}, Unauthorized", fail_msg=f"{status} / {body}")

    # 5️⃣ POST с правильными логином/паролем
    log("\n5️⃣ POST с правильными логином/паролем")
    status, body = req_post({"login": "admin", "password": "admin"})
    cond = (status == 200)
    has_computer = False
    if isinstance(body, list) and body:
        last = body[-1]
        has_computer = isinstance(last, dict) and "computer" in last
    check(cond and has_computer, "POST (admin/admin)", success_msg=f"код {status}, есть 'computer'", fail_msg=f"{status} / {body}")

    # 6️⃣ Проверка GET — должны быть данные
    log("\n6️⃣ GET — проверяем, что данные добавились")
    status, body = req_get()
    cond = (status == 200) and isinstance(body, list) and len(body) > 0
    check(cond, "GET после POST(admin)", success_msg=f"код {status}, {len(body)} элементов", fail_msg=f"{status} / {body}")

    # 7️⃣ Финальная очистка
    log("\n7️⃣ DELETE — финальная очистка")
    status, body = req_delete()
    check(status == 200, "DELETE (финальный)", success_msg=f"код {status}", fail_msg=f"{status} / {body}")

    log("\n=== ТЕСТ API ЗАВЕРШЁН ===")


def print_summary():
    total = len(results)
    passed = sum(1 for _, ok in results if ok)
    failed = total - passed
    log("\n📊 ИТОГ:")
    log(f"Всего тестов: {total}")
    log(f"✅ Успешных:  {passed}")
    log(f"❌ Провалено: {failed}")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    run_tests()
    print_summary()

