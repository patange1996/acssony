
import requests

r = requests.get('https://track.app.channeliq.com/api/wtb/redirect/8597af67-4f2a-4836-b8ae-1ec8fe402ec6/4?rurl=aHR0cHM6Ly9nb3RvLndhbG1hcnQuY29tL2MvMjIyMDQwMy81NjU3MDYvOTM4Mz9zdWJJZDE9YzUzM2EwMWIwM2I2NWEwOWFkNTI5ZTJjZjA2ODVmNzUmdmVoPWFmZiZzb3VyY2VpZD1pbXBfMDAwMDExMTEyMjIyMzMzMzQ0JnU9aHR0cHMlM0ElMkYlMkZ3d3cud2FsbWFydC5jb20lMkZpcCUyRlByZW1pZXItUHJvdGVpbi0xMDAtV2hleS1Qcm90ZWluLVBvd2Rlci1WYW5pbGxhLU1pbGtzaGFrZS0zMGctUHJvdGVpbi0yNC01LU96LTEtNS1MYiUyRjk0NTIzNTI0MQ%253d%253d&cpid=d6c86675-4c7b-4092-b3cd-9c9c99f67947&mpid=70fd16f7-fe91-4cd1-93cf-16b78ec26ea4&osk=c9a95439-43af-4d37-8791-0c05402a5ef3&zp=&vs=', allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"})


print(r.url)
