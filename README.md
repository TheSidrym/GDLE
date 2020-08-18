# GDLE
This repository should help automate level creation
# Example
``` python
    from GeometryDash import *
    # Main thing
    local = Local('CCLocalLevels.dat')
    level = Level()

    # Here you need to type name of level you will replace
    local.getLevelByName(input("Level Name: "))

    # Color adding example
    level.addColor(1,(255,0,0)) # Color with id 1 will be red
    level.addColor(2,(0,255,0)) # Color with id 2 will be green

    # Block adding example 1
    level.addBlock(Block({
        "id":1,
        "x":30, # First block x coordinate
        "y":15, # First block y coordinate
        "colorBase":1 # Base color id
    })())

    # Block adding example 2
    block = Block({
        "id":1
        "x":30
        "y":15
    })
    level.addBlock(block())

    # Saving changes
    q = input("Your current level save will be overwritten, are you sure about it? (y/n)")
    if q == "y":
        print("overwriting...")
        local.save(level())
        print("Completed.")
```