# Developer README

## Purpose and Scope

This document provides an overview of the Orchid Python API for developers. It models the overall 
structure of the package and its demo applications.

### WARNING: Just Sketches

The diagrams modeling our structure and collaborations are _just sketches_. The collaboration and class 
diagrams are not guaranteed to be consistent. Further, the author fully expects that implementing the package
 and demo applications will uncover details that are not covered by these UML models.

## Layers

The following diagram models the collaboration between classes and functions across layers of the application
 and package. Remember that, because Python does not require objects, a number of "classes" in the model may 
 simply be Python functions.

![Collaborations Across Layers](./layer-collaboration.png)

The next diagram models the classes and functions but assigns them to layers. Again, a class in the UML model 
may actually be a simple python function.

![Classes/Functions in Layers](./layer-structure.png)

Finally, the following diagram assigns classes to layers.

![Classes/Functions Assigned to Layers](./layer-classes.png)

## Components

This diagram describes the Orchid assembly dependencies for assemblies used by the Orchid Python API.

![Orchid Assembly Dependencies](./orchid-assy-dependencies.png)
