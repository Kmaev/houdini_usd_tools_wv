# WV (weave)– Tools for Houdini USD Pipelines

This repo is a growing collection of small utilities — aimed at improving workflows in Houdini.

---

## Currently Included

### USD Material Binding Validator
- A PySide based tool to inspect and fix missing material bindings.
- Allows searching and filtering prims with missing materials using a Trie-based search. 
- Displays prim details (name, path, type, bound material) in a detail view.
- Provides a material library browser and enables assigning materials to selected prims.
- Supports bulk assign to filtered primitives:
When the checkbox "Bulk assign material to all filtered" is enabled, the selected material
is applied to all filtered primitives, regardless of manual selection.

Demo Presentation:

https://vimeo.com/1093300593

<img width="1004" alt="image" src="https://github.com/user-attachments/assets/b939f8f4-fb51-4b10-80f2-8a63207afc13" />

Bulk assign materials based on filter:

<img width="1004" alt="image" src="https://github.com/user-attachments/assets/71d5c16f-1add-4b82-9422-17da12a0b8db" />

### USD Scene Template Generator

A utility that builds a structured USD scene from a declarative JSON file.

- Recursively generates prims (`Scope`, `Xform`, `Camera`)
- Supports optional `kind` metadata for asset tagging
- Designed to integrate easily into Houdini-based USD workflows
- Outputs organized, studio-ready USD layers

---
![img](https://github.com/user-attachments/assets/3e19a7f1-b01f-4d68-b9ad-1390bab2483b)


CLI Tool setup:

![img_1](https://github.com/user-attachments/assets/b176824c-6a91-4958-8b33-cce8558cc9cb)




