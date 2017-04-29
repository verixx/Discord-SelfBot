import asyncio
import json
import logging

log = logging.getLogger('LOG')
loop = asyncio.get_event_loop()
lock = asyncio.Lock()


def read_config(searched):
    with open('config/config.json', 'r') as f:
        cont = json.load(f)
        try:
            return cont[searched]
        except:
            return None


def read_log(searched):
    with open('config/log.json', 'r') as f:
        cont = json.load(f)
        try:
            return cont[searched]
        except:
            return None


def saving(file_name, field, value):
    with open('config/' + file_name, 'r') as q:
        content = json.load(q)
        secure_content = content
        with open('config/' + file_name, 'w') as f:
            try:
                content[field] = value
                f.seek(0)
                f.truncate()
                json.dump(content, f, indent=4, separators=(',', ':'))
                return True
            except:
                f.seek(0)
                f.truncate()
                json.dump(secure_content, f, indent=4, separators=(',', ':'))
                log.error("An Error occurd while saving")
                return False


async def save_config(field, value):
    with await lock:
        await loop.run_in_executor(None, saving, 'config.json', field, value)


async def save_log(field, value):
    with await lock:
        await loop.run_in_executor(None, saving, 'log.json', field, value)
