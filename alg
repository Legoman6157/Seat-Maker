b1:
    if outside of the bounds of closest square:
        is rectangle selecting

b1 motion:
    is rectangle selecting:
        clear previous drawn rectangle
        draw new rectangle with initial_click_pos as origin and current location
                as end point
        
    else:
        move selected squares

b1 release:
    is rectangle selecting:
        get a list of the shapes that intersect with the selection rectangle
        select all of those seats
        clear the selection rectangle
        is no longer rectangle selecting