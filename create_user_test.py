import sender_stand_request
import data
# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201;
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
           + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def negative_assert(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400;
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"
def negative_assert_no_first_name(user_body):
    user_body = get_user_body(user_body)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400;
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

def test_create_user_2_letter_in_first_name_get_success_response():
    return positive_assert("Aa")
def test_create_user_15_letter_in_first_name_get_success_response():
    return positive_assert("Asdfghnydkykrek")
def test_create_user_1_letter_in_first_name_get_error_response():
    return negative_assert("А")

def test_create_user_16_letter_in_first_name_get_error_response():
    return negative_assert("Asdfghnydkykrekd")
def test_create_user_english_letter_in_first_name_get_success_response():
    return positive_assert("Mary")
def test_create_user_russian_letter_in_first_name_get_success_response():
    return positive_assert("Маша")
def test_create_user_has_space_in_first_name_get_error_response():
    return negative_assert("Мария Ева")
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    return negative_assert("Мария%$%£")
def test_create_user_has_number_in_first_name_get_error_response():
    return negative_assert("Мария123")
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400

