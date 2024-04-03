Dataset **ArSL21L** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/P/S/bY/NI2gYP0QK32DZiTjX0ZnrrIJEDk97bRBHkJ3mxgEZ42rGDd2hlQXvfUwFZIYxcYLeLJSbHnW9hTZ7gvaeTsb2y09jWKt7V0ihlI6M0CZaCTiqRIGbm18IgACUY7Y.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='ArSL21L', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/f63xhm286w-1.zip).