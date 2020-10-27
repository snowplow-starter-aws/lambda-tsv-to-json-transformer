import base64
import json
from event_transformer import transform

print('Loading function')


def lambda_handler(event, context):
    output = []
    succeeded_record_cnt = 0
    failed_record_cnt = 0
    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data'])
        try:
            d = transform(payload.decode('utf-8'))

            payload = json.dumps(d) + "\n"
            succeeded_record_cnt += 1
            print(d)
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(payload.encode("utf-8")).decode("utf-8")
            }
        except Exception as ex:
            print(ex)
            print('Parsing failed')
            failed_record_cnt += 1
            output_record = {
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            }

        output.append(output_record)

    # print(output)
    print('Processing completed.  Successful records {}, Failed records {}.'.format(succeeded_record_cnt,
                                                                                    failed_record_cnt))
    return {'records': output}
