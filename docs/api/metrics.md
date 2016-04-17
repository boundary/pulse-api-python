Metrics
=======

_Metrics_ are


## `metric_create`

```
metric_create_batch(metric=None,
                    display_name=None,
                    display_name_short=None,
                    description=None,
                    default_aggregate='avg',
                    default_resolution=1000,
                    unit='number',
                    disable=False)
```


### Example

```
import tspapi

api = tspapi.API()
api.metric_create(name='Foo',
                  display_name='Foo',
                  display_name_Short='Foo'
                  description='A story about foo',
                  default_aggregate='max',
                  default_resolution=5000,
                  unit='percent',
                  disabled=False)
                        
```

## `metric_create_batch`

**metric_create_batch(measurements)**

### Example


## `metric_delete`


### Example

```
```

## `metric_get`

### Example

```
```

### Example

```
```

## `metric_update`


### Example

```
```
