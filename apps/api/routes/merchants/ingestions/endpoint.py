from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.routes.merchants.ingestions.repository import MerchantIngestRepository
from api.routes.merchants.llm_service import LLMService

import requests


@api_view(['POST'])
def injest(merchantType):

    pages = [
        {
            "id": "aef8ca90-05ef-4881-a8a8-3d090f7245be",
            "title": "Lanches"
        },
        {
            "id": "560ef60c-ed49-4343-a790-1ec9b1a40ec2",
            "title": "Pizza"
        },
        {
            "id": "313919a6-6406-4625-8a90-eef3bc0fad7c",
            "title": "Japonesa"
        },
        {
            "id": "f04f9c5d-8825-44c8-ba66-ff9865aa11d5",
            "title": "Brasileira"
        },
        {
            "id": "a7c10a46-19b1-4d25-9305-35b12fd5768c",
            "title": "Doces "
        },
        {
            "id": "4848c8d1-98f8-4c5d-a42f-11750e9ca4fe",
            "title": "Açaí"
        },
        {
            "id": "3c28b2aa-9f31-4e6f-b0aa-178f69fda3e8",
            "title": "Árabe"
        },
        {
            "id": "527c4614-6fca-45bc-abf3-c3c4d4cd622b",
            "title": "Salgados"
        },
        {
            "id": "22c1b0df-ef65-41fd-862b-c369bfdf588e",
            "title": "Sorvetes"
        },
        {
            "id": "57b265a4-61f0-4bd4-a99e-56ac45180605",
            "title": "Italiana"
        },
        {
            "id": "f5df081f-21c8-4ca6-8394-aa6a74c975fd",
            "title": "Padarias"
        },
        {
            "id": "106e9205-b217-4000-b609-31f48a4e9749",
            "title": "Chinesa"
        },
        {
            "id": "1dd45663-0318-44a2-98bd-951d38ba98e8",
            "title": "Gourmet"
        },
        {
            "id": "e6f0734f-990b-44f5-b94c-b43c86d36e52",
            "title": "Marmita"
        },
        {
            "id": "3e440c89-651a-48af-a6bc-9f46db5ca953",
            "title": "Saudável"
        },
        {
            "id": "5c8cecc3-4007-4b30-9926-9b66f76a166c",
            "title": "Pastel"
        },
        {
            "id": "a50ecfab-9db5-43ea-b3c4-b88c3b803ce2",
            "title": "Carnes"
        }
    ]
    repository = MerchantIngestRepository.create()
    service = LLMService()
    all_contents = []
    for page in pages:
        if 'id' in page:
            page_id = page['id']
            title = page['title']
            contents = fetch_contents(page_id, title, repository, service)
            print(title)
            all_contents.extend(contents)
   
    return Response(all_contents) 


def fetch_contents(page_id, title, repository: MerchantIngestRepository, embedding_service: LLMService):
    location = "latitude=YourLocation&longitude=YouLocation"
    url = 'https://marketplace.ifood.com.br/v1/page/{}?{}&channel=IFOOD'.format(page_id, location)
    headers = {
        'content-type': 'application/json',
    }
    payload = {
        'supported-headers': ['OPERATION_HEADER'],
        'supported-cards': [
            'MERCHANT_LIST',
            'CATALOG_ITEM_LIST',
            'CATALOG_ITEM_LIST_V2',
            'CATALOG_ITEM_LIST_V3',
            'FEATURED_MERCHANT_LIST',
            'CATALOG_ITEM_CAROUSEL',
            'CATALOG_ITEM_CAROUSEL_V2',
            'CATALOG_ITEM_CAROUSEL_V3',
            'BIG_BANNER_CAROUSEL',
            'IMAGE_BANNER',
            'MERCHANT_LIST_WITH_ITEMS_CAROUSEL',
            'SMALL_BANNER_CAROUSEL',
            'NEXT_CONTENT',
            'MERCHANT_CAROUSEL',
            'MERCHANT_TILE_CAROUSEL',
            'SIMPLE_MERCHANT_CAROUSEL',
            'INFO_CARD',
            'MERCHANT_LIST_V2',
            'ROUND_IMAGE_CAROUSEL',
            'BANNER_GRID',
            'MEDIUM_IMAGE_BANNER',
            'MEDIUM_BANNER_CAROUSEL',
            'RELATED_SEARCH_CAROUSEL',
            'ADS_BANNER',
        ],
        'supported-actions': [
            'catalog-item',
            'merchant',
            'page',
            'card-content',
            'last-restaurants',
            'webmiddleware',
            'reorder',
            'search',
            'groceries',
            'home-tab',
        ],
        'feedFeatureName': '',
        'fasterOverrides': '',
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        contents = []
        sections = response.json().get('sections', [])
        for section in sections:
            if section.get('cards'):
                for card in section['cards']:
                    if card.get('data') and card['data'].get('contents'):
                        for content in card['data']['contents'][:100]:
                            content = sanitize_content(content)
                            content['title'] = title
                            description_text_embedding = get_content_description(content)
                            content['description'] = description_text_embedding
                            content['content_description_embedding'] = embedding_service.generate_embedding(description_text_embedding)
                            repository.ingest(content)
                            contents.append(content)
                                

        return contents
    except requests.exceptions.RequestException as e:
        print('Error fetching data for page {}: {}'.format(page_id, e))
        return []
    
def sanitize_content(content):
    content.pop('contentDescription', None)
    content.pop('action', None)
    content.pop('adsMetadata', None)
    content.pop('distance', None)
    content.pop('isFavorite', None)
    return content

def get_content_description(content):
    delivery = ""
    if 'deliveryInfo' in content:
        delivery_info = content['deliveryInfo']
        if "timeMinMinutes" in delivery_info and "timeMaxMinutes" in delivery_info and "fee" in delivery_info:
            time_min_minutes = str(delivery_info['timeMinMinutes'])
            time_max_minutes = str(delivery_info['timeMaxMinutes'])
            fee = str(delivery_info['fee'] / 100)
            delivery = ", Entrega entre " + time_min_minutes + " e " + time_max_minutes  + " minutos, Taxa de entrega: " + fee

    description_text = content['name'] + ", Tipo de comida: " + content['mainCategory'] + delivery
    return description_text