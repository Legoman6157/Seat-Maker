import tkinter as tk

color_selected = "red"
color_unselected = "lightgray"

rects = []
temp_selected_seats = []
prev_temp_selected_seats = []
selected_seats = []
initial_click_pos = None
rectangle_select_active = False
selection_rectangle = None
rectangle_select_origin = None

row_descriptors = ['A', 'B', 'C', 'D']

def export_seats():
    global num_cols
    curr_col = 0
    row = 0

    o_f = open("seats.txt", "w")
    for rect in rects:
        coords = cv.coords(rect)

        o_f.write(f"{row_descriptors[row]},{curr_col+1},{1},{0},{int(coords[0])},{int(coords[1])},500,500,0,{row+1}")

        curr_col = curr_col + 1

        if curr_col == num_cols:
            o_f.write("\n")
            curr_col = 0
            row = row + 1
        else:
            o_f.write("\t")
    o_f.close()

def list_selected_seats():
    print(selected_seats)

def list_selected_rects():
    print(rects)

#Set up unselect all buttons, no matter what is selected
def unselect_all_seats(event=None):
    global selected_seats
    global initial_click_pos

    selected_seats.clear()
    initial_click_pos = None
    for rect in rects:
        cv.itemconfig(rect, outline=color_unselected)

app = tk.Tk()
app.title("Seat Maker")
app.geometry("1000x600")

num_rows = 4
num_cols = 5

main_frame = tk.Frame(app)
main_frame.pack()
grid_frame = tk.Frame(main_frame)
grid_frame.grid(row=0, column=1)


l = 20

x_offset = 0
y_offset = 0

cv = tk.Canvas(main_frame, width=800, height=600, background="gray")
cv.grid(column=0, row=0)

def click_and_drag_selected_seats(event):
    global temp_selected_seats
    global selected_seats
    global initial_click_pos
    global rectangle_select_active
    global selection_rectangle

    if rectangle_select_active:
        if selection_rectangle != None:
            cv.delete(selection_rectangle)
            selection_rectangle = None
            for seat in temp_selected_seats:
                cv.itemconfigure(seat, outline=color_unselected)
            temp_selected_seats.clear()

        x = cv.canvasx(event.x)
        y = cv.canvasy(event.y)

        selection_rectangle = cv.create_rectangle(initial_click_pos[0], initial_click_pos[1], event.x, event.y, outline=color_selected)
        temp_selected_seats = list(set(temp_selected_seats).union(set(cv.find_overlapping(initial_click_pos[0], initial_click_pos[1], event.x, event.y)[:-1])))

        for seat in temp_selected_seats:
            cv.itemconfigure(seat, outline=color_selected)

    else:
        if initial_click_pos == None:
            print("click_and_drag_selected_seats: initial_click_pos is set to None")
            return

        for selected_seat in selected_seats:

            coords = cv.coords(selected_seat)

            inner_x_offset = initial_click_pos[0] - coords[0]
            inner_y_offset = initial_click_pos[1] - coords[1]

            cv.move(selected_seat, event.x-coords[0]-inner_x_offset, event.y-coords[1] - inner_y_offset)

        initial_click_pos = (event.x, event.y)


def get_closest_seat(event):
    x = cv.canvasx(event.x)
    y = cv.canvasy(event.y)

    return rects[cv.find_closest(x, y)[0]-1]


def select_seat(seat):
    global selected_seats
    cv.itemconfigure(seat, outline=color_selected)
    if not seat in selected_seats:
        selected_seats.append(seat)


def unselect_seat(event=None, seat=None):
    global selected_seats

    if event != None and seat == None:
        seat = get_closest_seat(event)

    cv.itemconfigure(seat, outline=color_unselected)
    if seat in selected_seats:
        selected_seats.remove(seat)


def process_click(event):
    global selected_seats
    global initial_click_pos
    global rectangle_select_active

    x = cv.canvasx(event.x)
    y = cv.canvasy(event.y)

    closest_seat = rects[cv.find_closest(x, y)[0]-1]
    seat_coords = cv.coords(closest_seat)

    if (x > seat_coords[0]) and (x < seat_coords[0]+l) and \
       (y > seat_coords[1]) and (y < seat_coords[1]+l):
        select_seat(closest_seat)
    else:
        rectangle_select_active = True

    initial_click_pos = (event.x, event.y)


def canvas_click(event):
    unselect_all_seats()
    process_click(event)


def motion(event):

    x = cv.canvasx(event.x)
    y = cv.canvasy(event.y)

    closest_seat = rects[cv.find_closest(x, y)[0]-1]
    closest_seat_coords = cv.coords(closest_seat)

    if (abs(x - closest_seat_coords[0]) < 5) \
        and (abs(y - closest_seat_coords[1]) < 5):
        app.configure(cursor='tcross')
    else:
        app.configure(cursor='arrow')


def release_m1(event):
    global rectangle_select_active
    if selection_rectangle != None:
        cv.delete(selection_rectangle)

    for selected_seat in temp_selected_seats:
        select_seat(selected_seat)
    temp_selected_seats.clear()

    rectangle_select_active = False


cv.bind('<1>', canvas_click)
cv.bind('<Shift-1>', unselect_seat)
cv.bind('<Control-1>', process_click)
cv.bind('<B1-Motion>', click_and_drag_selected_seats)
cv.bind('<Motion>', motion)
cv.bind('<ButtonRelease-1>', release_m1)

for i in range(num_rows):
    for j in range(num_cols):
        temp_rect = cv.create_rectangle(x_offset, y_offset, x_offset+l, y_offset+l, fill="black", outline=color_unselected)
        rects.append(temp_rect)

        x_offset = x_offset + 40
    x_offset = 0
    y_offset = y_offset + 40

btn_frame = tk.Frame(grid_frame)
btn_frame.grid(column=1, row=0)

btn_export = tk.Button(btn_frame, text="Export", command=export_seats)
btn_export.pack()

btn_list_selected = tk.Button(btn_frame, text="List Selected", command=list_selected_seats)
btn_list_selected.pack()

btn_list_rects = tk.Button(btn_frame, text="List Rectangles", command=list_selected_rects)
btn_list_rects.pack()

app.bind_all('<Escape>', unselect_all_seats)

app.mainloop()
