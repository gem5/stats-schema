# stats-schema

A proposal for a shared statistics schema for computer architecture simulators.

Initially, we will be targeting the JSON output format, but we plan to support many other output formats in the future (e.g., CSV, HDF5, pandas, etc.).

This repository is currently maintained by Jason Lowe-Power <jason@lowepower.com>.
All questions/comments can be directed toward Jason via email or creating an issue on this repository.

The current working group members are

- Jonathan Beard (Arm)
- Bobby Bruce (gem5, UC Davis)
- Ahmed Gheith (Arm)
- Jason Lowe-Power (gem5, UC Davis)
- Andreas Sandberg (gem5, Arm)
- Arun Rodrigues (SST, Sandia)
- Gwen Voskuilen (SST, Sandia)

## Background

There are many computer architecture simulators (e.g., [gem5](http://www.gem5.org/), [SST](http://sst-simulator.org/), [DRAMSim](https://github.com/umd-memsys/DRAMsim3), and [GPGPU-Sim](http://www.gpgpu-sim.org/)), and each of them have their own output formats, which are often poorly defined.
This causes pain for researchers and students using these simulators.

Some pain points include:

- Writing custom text parsing code for each simulator (or multiple time for the same simulator!)
- Confusion on the meaning of statistics
- Incompatibility between simulators, especially when used together (e.g., gem5+DRAMSim)

**The goal of this working group is to define a common schema for computer architecture simulator statistics.**
With this common schema, we hope to enable better compatibility between simulators and to ease the burden on simulator users.

## This repository

This repository contains a proposal for a statistic schema using [JSON Schema](https://json-schema.org).

### JSON Schema

A good starting guide to JSON Schema is [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/index.html).
JSON Schema is most related to [database schemas](https://en.wikipedia.org/wiki/Database_schema) and simply defines the *format* of statistics.
Simulators must implement statistic output that follows this schema.

JSON Schema also has the ability to validate an output against the schema.
However, we expect that this schema will be used by the simulator developers to design their statistic outputs and by visualization developers to visualize and represent those output.
General simulator users shouldn't have to worry about this schema and can simply use the output from the simulators.

The file <statistic-output.schema.json> contains the current draft of the schema.

### Testing the schema

The <tests> directory contains a simple python script to test the schema.

To run the tests, you can use the following code:

```sh
pip3 install -r requirements.txt
cd tests
python3 test.py
```

This test will validate the schema.
Then, it will validate all of the files in <tests/examples>.
Details of these files can be found in the [README](tests/examples/README.md) in that directory.
It contains a set of valid and invalid examples of statistics files in json format.

## Understanding the schema file

The schema file begins with a title and description of the overall schema as well as some JSON Schema specific information.

Then, there is a section of "definitions."
These are "types" that can be used throughout the rest of the schema.
You can think of these as specializations of the built-in [JSON types](https://json-schema.org/understanding-json-schema/reference/type.html).

> Note: We may want to break this schema into multiple documents, which is possible to do in JSON Schema

Each of these types also has a title and a description.
This is the documentation for the user (simulator developer, in this case) to understand what this definition is supposed to represent.

For objects, we specify the *properties* that we expect these objects to have.
For the most part, properties are *optional* to support simpler/smaller/compressed files.
However, all statistics must have a `value`, and there are a few other required properties.
See comments in the schema for details.

### Style

> Note: We will almost certainly want to revisit this

#### Types

The current style for defining "types" is camel case with a lowercase first letter.

#### Property names

The current style for property names is camel case with a lowercase first letter.

------------

Below here is some older information

## Related works

### Some generally related works

- Generally, data serialization
- HPC serialization
  - Comprehensive Resource Use Monitoring for HPCSystems with TACC Stats
    - <https://www.tacc.utexas.edu/documents/1084364/1191938/tacc_stats_hust.pdf> (HPC users workshop)
    - No schema
  - Serialization and deserialization of complex data structures,and applications in high performance computing
    - <https://mosaic.mpi-cbg.de/docs/Zaluzhnyi2016.pdf> (masters thesis)
    - Avro
- System monitoring
  - Prometheus
    - <https://prometheus.io/>
    - Focused on time series
    - Doesn't have a set schema except for simple data types

### Projects

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

- <https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats>

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
