import io, json
import time

measurement_id = 0; 


def update(fill_percent):
		data = {}
		data['value'] = fill_percent
		with io.open('fill_level.json', 'w', encoding='utf-8') as f:
  				f.write(unicode(json.dumps(data, ensure_ascii=False)))
for x in range(100):
		update((1.0+x)/100.0); 
		time.sleep(0.05);