from unittest.mock import patch, MagicMock
from aiohttp import FormData
from http import HTTPStatus

import pytest
import json

async def test_index_page_contain_valid_multipart_form(client):
    response = await client.get('/')
    text = await response.text()
    assert response.status == HTTPStatus.OK, text
    assert 'method="post"' in text.lower(), 'У формы не указан POST метод'
    assert 'enctype="multipart/form-data"' in text.lower(), 'у формы не указан enctype'
    assert 'type="submit"' in text.lower(), 'у формы нет кнопки отправки'

@pytest.mark.parametrize('image_path,label_expected', [
    ('data_folder/3m2_cropped_0.png', 'm3'),
])
async def test_if_sent_image_then_label_and_cropped_image_appear_in_response(
        client,
        image_path,
        label_expected,
):
    form = FormData()
    form.add_field(
        name='image',
        value=open(image_path, 'rb'),
        content_type='image/jpeg',
        filename='3m2_cropped_0.png',
    )
    response = await client.post('/', data=form)
    text = await response.text()
    assert response.status == HTTPStatus.OK, text

    # Проверяем, что метка отображается в ответе
    assert label_expected.lower() in text.lower(), f'Expected label {label_expected} in response'

    # Проверяем, что обрезанное изображение и ближайшее похожее изображение есть в ответе
    assert '<img src="data:image/png;base64,' in text, 'Expected base64 image in response'

async def test_if_sent_faulty_image_then_error_appear_in_response(client):
    form = FormData()
    form.add_field(
        name='image',
        value=open('data_folder/3m1_cropped_0.png', 'rb'),
        content_type='image/jpeg',
        filename='3m1_cropped_0.png',
    )
    error_message = 'something nasty happened'
    yolo_model = client.app['yolo_model']
    feature_model = client.app['feature_model']

    yolo_mock = MagicMock(side_effect=ValueError(error_message))
    feature_mock = MagicMock(side_effect=ValueError(error_message))

    with patch.object(yolo_model, 'predict', yolo_mock), \
         patch.object(feature_model, 'forward', feature_mock):
        response = await client.post('/', data=form)
    text = (await response.text()).lower()
    assert response.status == HTTPStatus.OK, text
    assert error_message in text, f'expected {error_message} in {text}'
