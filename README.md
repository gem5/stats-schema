# stats-schema
A proposal for a shared statistics schema

## Related works

- Generally, data serialization
- HPC serialization
  - Comprehensive Resource Use Monitoring for HPCSystems with TACC Stats
    - https://www.tacc.utexas.edu/documents/1084364/1191938/tacc_stats_hust.pdf (HPC users workshop)
    - No schema
  - Serialization and deserialization of complex data structures,and applications in high performance computing
    - https://mosaic.mpi-cbg.de/docs/Zaluzhnyi2016.pdf (masters thesis)
    - Avro
- System monitoring

## Projects

- Advanced Scientific Data format (pronounced AZ-diff)
  - https://asdf-standard.readthedocs.io/en/1.5.0/index.html
  - For Astronomical data
- Apache Avro
  - Support for code auto generation
  - More about messages than data storage
- Json Schema
  - https://json-schema.org/
- Google Protocol Buffers and Apache Thrift
  - Note really a schema, but can specify a schema
- CDR (Common data representation)
  - Not human readable
  - Quite "industrial"
- ASN.1
  - For telecommunications (mostly)
- Data Documentation Initiative
  - https://ddialliance.org/
- USGS data dictionaries
  - https://www.usgs.gov/products/data-and-tools/data-management/data-dictionaries

## Other links

- https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats

## Requirements

The main purpose of this schema is documentation.
More people will look at this schema to define stats than machines will read it.

- Easy to understand for users who will be creating new stats
- Compatible with standard APIs for Python and other languages

### Requirements of our stats output

- Possible to make human readable (concise, clear, etc.)
- Possible to parse/write easily
  - pandas
  - json
  - hdf5
  - csv
- Compact

### Nice to haves

- Standardized, but compatibility with our tools (python, C++, etc) is the real requirement.

## The general schema:

- Base file
  - Contains global stats and other models
- Model
  - Has a type (e.g., "Cache", "CPU", etc.)
    - We could specialize this and have different types of models that match across simulators
  - Can contain models and statistics
- Statistic
  - Name
  - Type
  - Value
  - Unit
  - Description

## An example Json Schema approach

First, some data that we want to put in the schema:

Here's the system that generated this "data"

```python
my_system = System()
my_system.cpus = [TimingSimpleCPU() for i in range(2)]
my_system.l2_cache = L2Cache()
for cpu in my_system.cpus:
  cpu.tlb = X86TLB()
  cpu.l1_cache = L1Cache()
  cpu.l1_cache.connectMemSide(my_system.l2_cache)
```


```json
{
  "my_system": {
    "type": "System",
    "cpus": [
      {
        "type": "CPU",
        "committed_instructions": {
          "value": 0,
          "type": "Scalar",
          "unit": "Count",
          "description": "The number of instructions committed"
        },
        "tlb": {
          "type": "TLB",
          "data_hits": {
            "value": 0,
            "type": "Scalar",
            "unit": "Count",
            "description": "The number of hits from data accesses"
          },
          "inst_hits": {
            "value": 0,
            "type": "Scalar",
            "unit": "Count",
            "description": "The number of hits from instruction accesses"
          }
        },
        "l1_cache": {
          "type": "Cache",
          "miss_latency": {
            "type": "Distribution",
            "bins": [0, 1.0e-8, 2.0e-8, 3.0e-8],
            "value":[0, 0, 0, 0],
            "unit": "Time",
            "description": "Latency of cache misses (includes both reads & writes)"
          }
        }
      },
      {
        "tlb": {
          "type": "TLB",
          "data_hits": {
            "value": 0,
            "type": "Scalar",
            "unit": "Count",
            "description": "The number of hits from data accesses"
          },
          "inst_hits": {
            "value": 0,
            "type": "Scalar",
            "unit": "Count",
            "description": "The number of hits from instruction accesses"
          }
        },
        "l1_cache": {
          "type": "Cache",
          "miss_latency": {
            "type": "Distribution",
            "bins": [0, 1.0e-8, 2.0e-8, 3.0e-8],
            "value":[0, 0, 0, 0],
            "unit": "Time",
            "description": "Latency of cache misses (includes both reads & writes)"
          }
        }
      }
    ],
    "l2_cache": {
      "type": "Cache",
      "miss_latency": {
        "type": "Distribution",
        "bins": [0, 1.0e-8, 2.0e-8, 3.0e-8],
        "value":[0, 0, 0, 0],
        "unit": "Time",
        "description": "Latency of cache misses (includes both reads & writes)"
      }
    }
  }
}
```

Not all output formats of the stats have to have all of the data from the schema.
I think this is a key idea to enable this.

### Example of the base file

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://gem5.org/statistic-output.schema.json",
  "title": "Architecture Simulator Statistics",
  "description": "A set of statistcs or results output from a computer architecture simulation",
  "type": "object",
  "properties": {
    "creationTime": {
      "description": "The time this output was generated (wall clock time) in Date format",
      "type": "string",
      "format": "date-time"
    },
    "globalStatistics": {
      "description": "Statistics not associated with a particular model (e.g., total ticks, total instructions, etc.)",
      "type": "array",
      "items": { "$ref": "http://gem5.org/statistic.schema.json" }
    }
  },
  "additionalProperties": { "$ref": "http://gem5.org/model.schema.json" }
}
```

Could also do the follwing for additional properties and drop "globalStatistics".
This would allow us to say "The file contains a set of named stats and/or models with stats or other sub-models"

```json
{
  "additionalProperties": {
    "anyOf": [
      { "$ref": "http://gem5.org/model.schema.json" },
      { "$ref": "http://gem5.org/statistic.schema.json" },
      { "$ref": "http://gem5.org/scalar-statistic.schema.json" },
      { "$ref": "http://gem5.org/distribution-statistic.schema.json" }
    ]
  }
}
```

### Example for a general statistic

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://gem5.org/statistic.schema.json",
  "title": "Statistic",
  "description": "A single statistic output",
  "properties": {
    "type": {"type": "string" },
    "value": {},
    "unit": {"type": "string" },
    "description": {"type": "string" }
  },
  "required": ["value"]
}
```

### Example for a specific statistic (Scalar)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://gem5.org/scalar-statistic.schema.json",
  "title": "Scalar",
  "description": "A scalar statistic value (e.g., a count, latency, etc.)",
  "properties": {
    "type": { "const": "Scalar" },
    "value": { "type": "number" },
    "unit": {"type": "string" },
    "description": {"type": "string" }
  },
  "required": ["value"]
}
```

### Example for a specific statistic (Distribution)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://gem5.org/distribution-statistic.schema.json",
  "title": "Distribution",
  "description": "A distribution of statistic values",
  "properties": {
    "type": { "const": "Distribution" },
    "value": {
      "type": "array",
      "items": { "type": "integer", "minimum": 0 }
    },
    "bins": {
      "type": "array",
      "items": { "type": "number" }
    },
    "binSize": { "type": "number" },
    "numBins": { "type": "integer", "minimum": 1 },
    "unit": { "type": "string" },
    "description": { "type": "string" }
  },
  "required": ["value"]
}
```

### Example for a model

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://gem5.org/model.schema.json",
  "title": "Model",
  "description": "A simulated model which has statistics and possibly other sub models",
  "properties": {
    "type": { "type": "string" }
  },
  "additionalProperties": {
    "anyOf": [
      { "$ref": "http://gem5.org/model.schema.json" },
      { "$ref": "http://gem5.org/statistic.schema.json" },
      {
        "type": "array",
        "items": {
          "type": { "$ref": "http://gem5.org/model.schema.json" }
        }
      }
    ]
  }
}
```

## Ideas

- We can have generic model which have "shared" stats between simulators (and other things)
  - E.g., Caches
    - Just hits/misses
    - Keep it simple
- We allow simulators to have more specific stats
- Allow for the simulator to output once the metadata and then simply output the values in all other outputs.
  - Want to have dynamic components
  - Need to support stats appearing in the middle of simulation
- Still need to define "alternative" schemas
  - CSV
  - ???

### Other potential info to include

- Data type of the result (e.g., u64, s32, f32)
  - The other option is to just use "integer" and "number" from json schema
- Other metadata with each dump/file

## Other questions to answer or potential features

- How to represent time-series data
  - How to "tag" each dump
- Dump different stats at different frequencies
  - How to represent this in the above schema
  - gem5 doesn't currently support this (easily), but could be extended
