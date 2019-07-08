import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.googleapis.com/drive/v3/files/13G8TBngSsblSf6rLhQ6tazfdYLct2h5l?alt=media&key=AIzaSyBJkR_8bc-4RRSjMAfhhVbvAoKAKHsjxZ4'
export_file_name = 'export.pkl'

classes = ['AM_General_Hummer_SUV_2000',
 'Acura_RL_Sedan_2012',
 'Acura_TL_Sedan_2012',
 'Acura_TL_Type-S_2008',
 'Acura_TSX_Sedan_2012',
 'Acura_Integra_Type_R_2001',
 'Acura_ZDX_Hatchback_2012',
 'Aston_Martin_V8_Vantage_Convertible_2012',
 'Aston_Martin_V8_Vantage_Coupe_2012',
 'Aston_Martin_Virage_Convertible_2012',
 'Aston_Martin_Virage_Coupe_2012',
 'Audi_RS_4_Convertible_2008',
 'Audi_A5_Coupe_2012',
 'Audi_TTS_Coupe_2012',
 'Audi_R8_Coupe_2012',
 'Audi_V8_Sedan_1994',
 'Audi_100_Sedan_1994',
 'Audi_100_Wagon_1994',
 'Audi_TT_Hatchback_2011',
 'Audi_S6_Sedan_2011',
 'Audi_S5_Convertible_2012',
 'Audi_S5_Coupe_2012',
 'Audi_S4_Sedan_2012',
 'Audi_S4_Sedan_2007',
 'Audi_TT_RS_Coupe_2012',
 'BMW_ActiveHybrid_5_Sedan_2012',
 'BMW_1_Series_Convertible_2012',
 'BMW_1_Series_Coupe_2012',
 'BMW_3_Series_Sedan_2012',
 'BMW_3_Series_Wagon_2012',
 'BMW_6_Series_Convertible_2007',
 'BMW_X5_SUV_2007',
 'BMW_X6_SUV_2012',
 'BMW_M3_Coupe_2012',
 'BMW_M5_Sedan_2010',
 'BMW_M6_Convertible_2010',
 'BMW_X3_SUV_2012',
 'BMW_Z4_Convertible_2012',
 'Bentley_Continental_Supersports_Conv._Convertible_2012',
 'Bentley_Arnage_Sedan_2009',
 'Bentley_Mulsanne_Sedan_2011',
 'Bentley_Continental_GT_Coupe_2012',
 'Bentley_Continental_GT_Coupe_2007',
 'Bentley_Continental_Flying_Spur_Sedan_2007',
 'Bugatti_Veyron_16.4_Convertible_2009',
 'Bugatti_Veyron_16.4_Coupe_2009',
 'Buick_Regal_GS_2012',
 'Buick_Rainier_SUV_2007',
 'Buick_Verano_Sedan_2012',
 'Buick_Enclave_SUV_2012',
 'Cadillac_CTS-V_Sedan_2012',
 'Cadillac_SRX_SUV_2012',
 'Cadillac_Escalade_EXT_Crew_Cab_2007',
 'Chevrolet_Silverado_1500_Hybrid_Crew_Cab_2012',
 'Chevrolet_Corvette_Convertible_2012',
 'Chevrolet_Corvette_ZR1_2012',
 'Chevrolet_Corvette_Ron_Fellows_Edition_Z06_2007',
 'Chevrolet_Traverse_SUV_2012',
 'Chevrolet_Camaro_Convertible_2012',
 'Chevrolet_HHR_SS_2010',
 'Chevrolet_Impala_Sedan_2007',
 'Chevrolet_Tahoe_Hybrid_SUV_2012',
 'Chevrolet_Sonic_Sedan_2012',
 'Chevrolet_Express_Cargo_Van_2007',
 'Chevrolet_Avalanche_Crew_Cab_2012',
 'Chevrolet_Cobalt_SS_2010',
 'Chevrolet_Malibu_Hybrid_Sedan_2010',
 'Chevrolet_TrailBlazer_SS_2009',
 'Chevrolet_Silverado_2500HD_Regular_Cab_2012',
 'Chevrolet_Silverado_1500_Classic_Extended_Cab_2007',
 'Chevrolet_Express_Van_2007',
 'Chevrolet_Monte_Carlo_Coupe_2007',
 'Chevrolet_Malibu_Sedan_2007',
 'Chevrolet_Silverado_1500_Extended_Cab_2012',
 'Chevrolet_Silverado_1500_Regular_Cab_2012',
 'Chrysler_Aspen_SUV_2009',
 'Chrysler_Sebring_Convertible_2010',
 'Chrysler_Town_and_Country_Minivan_2012',
 'Chrysler_300_SRT-8_2010',
 'Chrysler_Crossfire_Convertible_2008',
 'Chrysler_PT_Cruiser_Convertible_2008',
 'Daewoo_Nubira_Wagon_2002',
 'Dodge_Caliber_Wagon_2012',
 'Dodge_Caliber_Wagon_2007',
 'Dodge_Caravan_Minivan_1997',
 'Dodge_Ram_Pickup_3500_Crew_Cab_2010',
 'Dodge_Ram_Pickup_3500_Quad_Cab_2009',
 'Dodge_Sprinter_Cargo_Van_2009',
 'Dodge_Journey_SUV_2012',
 'Dodge_Dakota_Crew_Cab_2010',
 'Dodge_Dakota_Club_Cab_2007',
 'Dodge_Magnum_Wagon_2008',
 'Dodge_Challenger_SRT8_2011',
 'Dodge_Durango_SUV_2012',
 'Dodge_Durango_SUV_2007',
 'Dodge_Charger_Sedan_2012',
 'Dodge_Charger_SRT-8_2009',
 'Eagle_Talon_Hatchback_1998',
 'FIAT_500_Abarth_2012',
 'FIAT_500_Convertible_2012',
 'Ferrari_FF_Coupe_2012',
 'Ferrari_California_Convertible_2012',
 'Ferrari_458_Italia_Convertible_2012',
 'Ferrari_458_Italia_Coupe_2012',
 'Fisker_Karma_Sedan_2012',
 'Ford_F-450_Super_Duty_Crew_Cab_2012',
 'Ford_Mustang_Convertible_2007',
 'Ford_Freestar_Minivan_2007',
 'Ford_Expedition_EL_SUV_2009',
 'Ford_Edge_SUV_2012',
 'Ford_Ranger_SuperCab_2011',
 'Ford_GT_Coupe_2006',
 'Ford_F-150_Regular_Cab_2012',
 'Ford_F-150_Regular_Cab_2007',
 'Ford_Focus_Sedan_2007',
 'Ford_E-Series_Wagon_Van_2012',
 'Ford_Fiesta_Sedan_2012',
 'GMC_Terrain_SUV_2012',
 'GMC_Savana_Van_2012',
 'GMC_Yukon_Hybrid_SUV_2012',
 'GMC_Acadia_SUV_2012',
 'GMC_Canyon_Extended_Cab_2012',
 'Geo_Metro_Convertible_1993',
 'HUMMER_H3T_Crew_Cab_2010',
 'HUMMER_H2_SUT_Crew_Cab_2009',
 'Honda_Odyssey_Minivan_2012',
 'Honda_Odyssey_Minivan_2007',
 'Honda_Accord_Coupe_2012',
 'Honda_Accord_Sedan_2012',
 'Hyundai_Veloster_Hatchback_2012',
 'Hyundai_Santa_Fe_SUV_2012',
 'Hyundai_Tucson_SUV_2012',
 'Hyundai_Veracruz_SUV_2012',
 'Hyundai_Sonata_Hybrid_Sedan_2012',
 'Hyundai_Elantra_Sedan_2007',
 'Hyundai_Accent_Sedan_2012',
 'Hyundai_Genesis_Sedan_2012',
 'Hyundai_Sonata_Sedan_2012',
 'Hyundai_Elantra_Touring_Hatchback_2012',
 'Hyundai_Azera_Sedan_2012',
 'Infiniti_G_Coupe_IPL_2012',
 'Infiniti_QX56_SUV_2011',
 'Isuzu_Ascender_SUV_2008',
 'Jaguar_XK_XKR_2012',
 'Jeep_Patriot_SUV_2012',
 'Jeep_Wrangler_SUV_2012',
 'Jeep_Liberty_SUV_2012',
 'Jeep_Grand_Cherokee_SUV_2012',
 'Jeep_Compass_SUV_2012',
 'Lamborghini_Reventon_Coupe_2008',
 'Lamborghini_Aventador_Coupe_2012',
 'Lamborghini_Gallardo_LP_570-4_Superleggera_2012',
 'Lamborghini_Diablo_Coupe_2001',
 'Land_Rover_Range_Rover_SUV_2012',
 'Land_Rover_LR2_SUV_2012',
 'Lincoln_Town_Car_Sedan_2011',
 'MINI_Cooper_Roadster_Convertible_2012',
 'Maybach_Landaulet_Convertible_2012',
 'Mazda_Tribute_SUV_2011',
 'McLaren_MP4-12C_Coupe_2012',
 'Mercedes-Benz_300-Class_Convertible_1993',
 'Mercedes-Benz_C-Class_Sedan_2012',
 'Mercedes-Benz_SL-Class_Coupe_2009',
 'Mercedes-Benz_E-Class_Sedan_2012',
 'Mercedes-Benz_S-Class_Sedan_2012',
 'Mercedes-Benz_Sprinter_Van_2012',
 'Mitsubishi_Lancer_Sedan_2012',
 'Nissan_Leaf_Hatchback_2012',
 'Nissan_NV_Passenger_Van_2012',
 'Nissan_Juke_Hatchback_2012',
 'Nissan_240SX_Coupe_1998',
 'Plymouth_Neon_Coupe_1999',
 'Porsche_Panamera_Sedan_2012',
 'Ram_C/V_Cargo_Van_Minivan_2012',
 'Rolls-Royce_Phantom_Drophead_Coupe_Convertible_2012',
 'Rolls-Royce_Ghost_Sedan_2012',
 'Rolls-Royce_Phantom_Sedan_2012',
 'Scion_xD_Hatchback_2012',
 'Spyker_C8_Convertible_2009',
 'Spyker_C8_Coupe_2009',
 'Suzuki_Aerio_Sedan_2007',
 'Suzuki_Kizashi_Sedan_2012',
 'Suzuki_SX4_Hatchback_2012',
 'Suzuki_SX4_Sedan_2012',
 'Tesla_Model_S_Sedan_2012',
 'Toyota_Sequoia_SUV_2012',
 'Toyota_Camry_Sedan_2012',
 'Toyota_Corolla_Sedan_2012',
 'Toyota_4Runner_SUV_2012',
 'Volkswagen_Golf_Hatchback_2012',
 'Volkswagen_Golf_Hatchback_1991',
 'Volkswagen_Beetle_Hatchback_2012',
 'Volvo_C30_Hatchback_2012',
 'Volvo_240_Sedan_1993',
 'Volvo_XC90_SUV_2007',
 'smart_fortwo_Convertible_2012']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
