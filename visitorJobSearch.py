import requests
import re
import json
import sys
from auth import get_cookies

#Function that fetches job data from the upwork server.
def get_jobs(jobQuery):
    
    print('3 recieved request for jobs')   
    try:
        with open('cookies.json', 'r') as json_file:
            cookies = json.load(json_file)
            print("fetching cookies from file")
    except:
        print('Got error because of empty json file')
        get_cookies(jobQuery)
        return get_jobs(jobQuery)
        
    auth = cookies.get('UniversalSearchNuxt_vt', 'ERROR')
    
    if not auth or auth == 'ERROR':
        print('Auth not found')
        get_cookies(jobQuery)
        print('4 going again in get_jobs')
        return get_jobs(jobQuery)
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8,ur;q=0.7',
        'authorization': f'Bearer {auth}',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.upwork.com',
        'priority': 'u=1, i',
        'referer': f'https://www.upwork.com/nx/search/jobs/?nav_dir=pop&q={jobQuery}',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"145.0.7632.116"',
        'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.116", "Chromium";v="145.0.7632.116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '""',
        'sec-ch-viewport-width': '573',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'vnd-eo-parent-span-id': 'd7a3c6e9-314c-4ea3-a0cd-14595abc3012',
        'vnd-eo-span-id': '302dea3d-47e0-418a-8d62-a4aed043196a',
        'vnd-eo-trace-id': '9d5ed99857c13890-PDX',
        'vnd-eo-visitorid': '72.255.52.73.1770603153789000',
        'x-upwork-accept-language': 'en-US',
        # 'cookie': 'visitor_id=72.255.52.73.1770603153789000; x-spec-id=bfa27344-5342-45b9-b87f-f1d04c9b3968; device_view=full; spt=bce15f09-cf07-4612-b114-c83fd73b0ce3; _cq_duid=1.1770603173.uXAgsRNU66DycS2J; _gcl_au=1.1.120120299.1770603173; recognized=5427f5b7; company_last_accessed=d1017661746; OptanonAlertBoxClosed=2026-02-09T02:13:32.612Z; _vwo_uuid_v2=DF5A1F91939138DC0E2C0E3C682D9BC8A|91e59e72b7055cc7558439079e843443; _vwo_uuid=DF5A1F91939138DC0E2C0E3C682D9BC8A; _ga=GA1.2.1614004628.1771835924; ftr_ncd=6; _vis_opt_s=4%7C; up_g_one_tap_closed=true; _vwo_ds=3%241771829417%3A37.26188748%3A%3A%3A%3A%3A1772381931%3A1772363503%3A8; visitor_signup_gql_token=oauth2v2_int_f7fedb409ed8fe1272c06c94168a08d6; visitor_gql_token=oauth2v2_int_37b64f6bc37c50fb9dcd52fb10053e00; SeoPagesNuxt_vt=oauth2v2_int_27b23114321793c83b6ab9d86b8a0d3e; country_code=PK; _cq_suid=1.1772425597.inrbTLGeNeZKTzvq; _cfuvid=t9_uYHPxdmfJ59Cbi.muBgY0Ml_2mP.ZuDEoUPiI9MY-1772427333600-0.0.1.1-604800000; enabled_ff=!CI10270Air2Dot5QTAllocations,!CI10857Air3Dot0,!CI12577UniversalSearch,!MP16400Air3Migration,!SSINavUser,!SecAIBnrOn,!air2Dot76Qt,!i18nGA,CI11132Air2Dot75,CI17409DarkModeUI,CI9570Air2Dot5,JPAir3,OTBnrOn,SSINavUserBpa,TONB2256Air3Migration,air2Dot76,i18nOn; cookie_prefix=; cookie_domain=.upwork.com; __cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbbbZEU66oyndh; _upw_ses.5831=*; umq=573; DA_5427f5b7=11ce83f87bed27785a12db4bb75619511576d60da2be88c9f3dfef9db9e74450; 7ee7e6a9sb=oauth2v2_int_bb61d641ab7b4dcae7845b4eca8eb344; FindWorkHome:freelancerMenuSpacing=0px; FindWorkHome:hasInterviewsOrOffers=0; 4d58f854sb=oauth2v2_int_62c495e7065c7ee650aeb0a64c416dfd; asct_vt=oauth2v2_int_bf705ae80d48ba66b962db5d2c551be1; XSRF-TOKEN=cbf7d27c46114c58d3544e16b524c8f9; g_state={"i_l":0,"i_ll":1772433614829,"i_e":{"enable_itp_optimization":16},"i_b":"IPG2CR+pFrL13vA4jdwrxqIn8/0qBBwo8b9GEJgP5gU"}; __cf_bm=gBpMXNd26fBfsBtbEo5XXbb6HSgpnCt6dxeWvzXOxaQ-1772437665-1.0.1.1-WeMb62FloM43rQ3ZZJd1SQdU5icQM2rGGZlHc5Cu1DszgXXDe2oJumgCyS7eeH_CWNjLi11VICcMX7WD.19G84o3rCZP.46m0JEK09.yrMI; UniversalSearchNuxt_vt=oauth2v2_int_e5ba180ed660d17699f11b198bb00185; AWSALBTG=7/mJ0FcPTsb6QfyTcdlXhHLTGwPmRk6V/mmTONimlwY55GO9eQopIosZyIwamVnPVZhXeWgsHYFZ9Lx+DQrKvKaynwiaXThuWmDWfvQVbTclw7xQleJA1cxW/KP0fwyQK//w6uXFkFic1Pi0+0EVX6JbTMUlw8RRZR8F3Dg33jww; AWSALBTGCORS=7/mJ0FcPTsb6QfyTcdlXhHLTGwPmRk6V/mmTONimlwY55GO9eQopIosZyIwamVnPVZhXeWgsHYFZ9Lx+DQrKvKaynwiaXThuWmDWfvQVbTclw7xQleJA1cxW/KP0fwyQK//w6uXFkFic1Pi0+0EVX6JbTMUlw8RRZR8F3Dg33jww; cf_clearance=.Za7ro0xZYTak3vbnmQLw3.Z2doAduq34R7jnYklO7g-1772438244-1.2.1.1-SQqvWz5y_SkyHAo3PiFjjIG.3zmBwIlVwG1ZfEDAMjlqNd.KdtrCc.IdwL2IleTM_EbWMLPcH4TLNVWMTa73qD3EmRwTzdWaHopp8fV89UATYtKWD79zlHoUrBoIPe5ED5_4WyxLMmOSWyZmP52ZbHYawLsmEbmiQr450iSsDuyvk.kW813krIYJhOMJXpRzG36ML06uq7Sk40qJCDVmkSQRNOTo5EEx_riU_xWNEEURBm9Tm3suKuSppnD9AHz4; OptanonConsent=consentId=1543226884689084416&datestamp=Mon+Mar+02+2026+12%3A57%3A27+GMT%2B0500+(Pakistan+Standard+Time)&version=202512.1.0&isAnonUser=1&isGpcEnabled=0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&interactionCount=5&iType=undefined&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A1%2CC0004%3A0&crTime=1772433569777&intType=&geolocation=PK%3BPB&AwaitingReconsent=false; forterToken=d51aa35041464c24911033552d71f8da_1772438244357_1931_UDF43-m4_23ck_/C43KEyBUr4%3D-14571-v2; forterToken=d51aa35041464c24911033552d71f8da_1772438244357_1931_UDF43-m4_23ck_/C43KEyBUr4%3D-14571-v2; _upw_id.5831=93969871-d072-4372-9bd1-46597a61c3b6.1770603157.23.1772438255.1772427506.0c2a8a4a-2768-4819-8303-e81c874a8be0.b8c292dc-820f-43e4-9025-0dacd6f7e15b.c9743e46-1ac3-4416-becf-f0d89d27e2d3.1772429611622.338; AWSALB=EmyV690IHqLpRunvCeiEswuqPOhyBFUuAUO7FlCjrChh5VF2K1pem1Z9ee8qBJ9dlXJbnAs0SFXvjx3LYOyMM5B6K8V2UARfS+d+GaUA2vyWwDmZayLStjtZRZce; AWSALBCORS=EmyV690IHqLpRunvCeiEswuqPOhyBFUuAUO7FlCjrChh5VF2K1pem1Z9ee8qBJ9dlXJbnAs0SFXvjx3LYOyMM5B6K8V2UARfS+d+GaUA2vyWwDmZayLStjtZRZce',
    }

    params = {
        'alias':'visitorJobSearch',
    }

    json_data = {
        'query': '\n  query VisitorJobSearch($requestVariables: VisitorJobSearchV1Request!) {\n    search {\n      universalSearchNuxt {\n        visitorJobSearchV1(request: $requestVariables) {\n          paging {\n            total\n            offset\n            count\n          }\n          \n    facets {\n      jobType \n    {\n      key\n      value\n    }\n  \n      workload \n    {\n      key\n      value\n    }\n  \n      clientHires \n    {\n      key\n      value\n    }\n  \n      durationV3 \n    {\n      key\n      value\n    }\n  \n      amount \n    {\n      key\n      value\n    }\n  \n      contractorTier \n    {\n      key\n      value\n    }\n  \n      contractToHire \n    {\n      key\n      value\n    }\n  \n      \n    }\n  \n          results {\n            id\n            title\n            description\n            relevanceEncoded\n            ontologySkills {\n              uid\n              parentSkillUid\n              prefLabel\n              prettyName: prefLabel\n              freeText\n              highlighted\n            }\n            \n            jobTile {\n              job {\n                id\n                ciphertext: cipherText\n                jobType\n                weeklyRetainerBudget\n                hourlyBudgetMax\n                hourlyBudgetMin\n                hourlyEngagementType\n                contractorTier\n                sourcingTimestamp\n                createTime\n                publishTime\n                \n                hourlyEngagementDuration {\n                  rid\n                  label\n                  weeks\n                  mtime\n                  ctime\n                }\n                fixedPriceAmount {\n                  isoCurrencyCode\n                  amount\n                }\n                fixedPriceEngagementDuration {\n                  id\n                  rid\n                  label\n                  weeks\n                  ctime\n                  mtime\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n  ',
        'variables': {
            'requestVariables': {
                'userQuery': jobQuery,
                'sort': 'relevance+desc',
                'highlight': True,
                'paging': {
                    'offset': 0,
                    'count': 30,
                },
            },
        },
    }

    print('about to fetch response')
    response = requests.post(
        'https://www.upwork.com/api/graphql/v1',
        params=params,
        cookies=cookies,
        headers=headers, 
        json=json_data
        )

    print('response fetched')
    if response.status_code == 200 and response.text.strip():
        
        data = response.json()
        
        job_results = []
            
        results = data['data']['search']['universalSearchNuxt']['visitorJobSearchV1']['results']

        print('started loop for job info')
        for job in results:
            job_details = job['jobTile']['job']
            time = job_details['publishTime'][:16]
            job_info = {
                    "cipherID" : job_details['ciphertext'],
                    "title": re.sub(r'H\^|\^H', '', job['title']),
                    "time":  re.sub('T', ',', time),
                    "level": job_details['contractorTier'],
                    "budget": job_details['hourlyBudgetMax'],
                    "description": re.sub(r'H\^|\^H', '', job['description'])
                }
            job_results.append(job_info)
        print('done making list')
        return (job_results)
    
    
    else:
        print("Response Error")
        get_cookies(jobQuery)
        return get_jobs(jobQuery)