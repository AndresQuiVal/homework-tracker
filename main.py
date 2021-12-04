from general import TASKS_FILE_NAME, LAPSE_TASLS_FILE_NAME, VERSION, set_general_config, clear_console
import time
import csv
import math

def main():
    """
    Prints the menu and initializes required configurations
    """
    while True:
        clear_console()
        menu_option = input(f"""
    Homework Tracker {VERSION} ---------------------------------

    1) Ver calendario
    2) Configuración de la aplicación
    3) Agregar tareas
    4) Salir

    (Introduce el número) > """)
        clear_console()
        if menu_option == "1":
            show_calendar()
        elif menu_option == "2":
            show_conf_menu()
        elif menu_option == "3":
            show_add_tasks_menu()
        else:
            break

def show_calendar():
    """
    Shows the calendar of the tasks considering the lapse tasks
    """

    def get_busy_blocks_time():
        """
        Gets from lapse_tasks.csv busy blocks of time
        """
        with open(f'./data/{LAPSE_TASLS_FILE_NAME}', 'r') as f:
            tasks = list(csv.DictReader(f))
        
        return tasks
        
    def get_tasks_from_day(day, tasks):
        """
        Gets a list of tasks which are from a specific given day
        """

        output = []
        for task in tasks:
            if task['deliver_date'].lower() == day.lower():
                output.append(task)
        
        return output


    def get_available_task_for_time(free_time, tasks_of_day):
        """
        Gets the task which estimated_time is lesser or equal than the given free_time argument
        """

        for task in tasks_of_day:
            estimated_time = int(task['estimated_time'])
            if estimated_time <= free_time: 
                return task

    # import pdb; pdb.set_trace()
    tasks = []
    with open(f'./data/{TASKS_FILE_NAME}', 'r') as f:
        tasks = list(csv.DictReader(f))
    
    days = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
    busy_blocks_time = get_busy_blocks_time()

    busy_blocks_time.append({ # final block
        'name' : 'default', 
        'start' : 1440, 
        'end' : 1440
    })

    for day in days:
        print(f"\n{day} ------------------------------------------------- ")
        tasks_of_day = get_tasks_from_day(day, tasks) # list of dictionaries
        
        if len(busy_blocks_time) == 1:
            for task in tasks_of_day:
                print(f"Tarea: {task['name']}, tiempo estimado: {task['estimated_time']}")
            continue

        for i in range(len(busy_blocks_time) - 1):
            free_time = int(busy_blocks_time[i + 1]['start']) - int(busy_blocks_time[i]['end'])
            print(f"Bloque ocupado, Nombre: {busy_blocks_time[i]['name']}, tiempo: ({int(busy_blocks_time[i]['end']) - int(busy_blocks_time[i]['start'])})")

            while free_time > 0:
                enabled_task = get_available_task_for_time(free_time, tasks_of_day)
                if not enabled_task: # there's no tasks that "fits" the calculated free time
                    print(f"Bloque de tiempo libre disponible: {free_time}")
                    break
                    
                tasks_of_day.remove(enabled_task) # !
                free_time -= int(enabled_task['estimated_time'])
                
                print(f"Tarea: {enabled_task['activity']}, tiempo estimado: {enabled_task['estimated_time']}")
    
    input("\nPresiona enter para finalizar > ")
        


def show_conf_menu():
    # configurations such as reserved times
    # which specifies the amount of minutes where you have school, work, or occupied time
    
    def add_lapse_task():
        """
        Function for adding lapse tasks into lapse_tasks.csv
        """

        def already_exist(obj):
            """
            Checks if the task already exists
            """
            with open(f'./data/{LAPSE_TASLS_FILE_NAME}','r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['name'] == obj[0] or (obj[1] <= int(row['end']) and obj[1] >= int(row['start'])) or (obj[2] <= int(row['end']) and obj[2] >= int(row['start'])):
                        return True

            return False

        while True:
            name = input("Introduce el nombre: ")
            start = input("Introduce el tiempo de inicio (en minutos): ")
            end = input("Introduce el tiempo de fin (en minutos): ")

            try:
                start, end = int(start), int(end)
                if not name: raise ValueError()
            except ValueError:
                print("¡Los datos introducidos son incorrectos, intenta de nuevo!")
                continue
            else: 
                if already_exist([name, start, end]):
                    print("¡Ya existe un registro con los datos introducidos, intenta de nuevo!")
                    continue

                # add to database
                with open(f'./data/{LAPSE_TASLS_FILE_NAME}','a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, start, end])
                
                print("Tiempo reservado agregado!")
                time.sleep(3)
                break
    
    while True:
        clear_console()
        option = input("""
        Introduce la configuración a realizar:
        
        1) Agregar lapso de tiempo reservado
        2) Salir
        (Introduce el número) > """)

        clear_console()
        if option == "1":
            add_lapse_task()
        else: 
            break



def show_add_tasks_menu():
    while True:
        name = input("Introduce el nombre de la tarea: ")
        try:
            estimated_time = int(input("Introduce el tiempo estiamdo (en minutos): "))
        except ValueError:
            print("¡Introduce un número!")
            continue
        deliver_date = input("Introduce el día estimado de entrega (Lunes, Martes, Miercoles, Jueves, Viernes): ").lower()

        if deliver_date not in {"lunes","martes","miercoles","jueves","viernes"}:
            print("¡Introduce un día válido!")
        elif not estimated_time or not name:
            print("¡Introduce valores válidos para las entradas requeridas!")        
        else:
            # add to database
            with open(f'./data/{TASKS_FILE_NAME}','a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, estimated_time, deliver_date])
            
            print("¡Tarea agregada!")
            time.sleep(3)
            break


if __name__ == "__main__": # Entry point of the program.
    set_general_config()
    main()
