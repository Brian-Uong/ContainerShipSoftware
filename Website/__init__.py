import os, sys
from flask import Flask, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from load.manifest_read import parse
from load.balance import Tree
from load.instruction_read import iparse
from load.fix_astar import LTree
from load.manifest_read import A_Container

def create_app():

    UPLOAD_FOLDER = '/'

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key BEAM'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')  

    @app.route('/')
    def home():
        session['previous_url'] = url_for('home')
        outbound_Folder = os.listdir("Website\outbound")
        if(outbound_Folder[0]):
            outbound_name = outbound_Folder[0]
            outbound_file_path = os.path.join(app.root_path + '\outbound', outbound_name)
            os.unlink(outbound_file_path)
        return "Home Page"

    @app.route('/log', methods=['POST'])
    def log_message():
        log_message = request.form.get('logMessage')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + log_message + '\n')

        return redirect(session['previous_url'])
    
    @app.route('/signIn', methods=['POST'])
    def sign_in():
        sign_in = request.form.get('empName')
        file_path = 'log.txt'
        current_employee_path = 'curr_emp.txt'

        if not os.path.exists(current_employee_path):
            with open(current_employee_path, 'w') as f:
                f.write('')
        try:
            with open(current_employee_path, 'r') as f:
                previous_employee = f.read().strip()
        except FileNotFoundError:
            previous_employee = None
        if previous_employee:
            with open(file_path, 'a') as files:
                files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + previous_employee + ' signs out.\n')
        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')
        with open(current_employee_path, 'w') as f:
            f.write(sign_in)

        return redirect(session['previous_url'])
    
    @app.route('/homeRedirect', methods=['POST'])
    def homeRedirect():    
        session['previous_url'] = url_for('home')
        return redirect(url_for('auth.home'))

    #These both take a file from their respective buttons on the home page and upload it to the ManifestFolder file. If there is no file selected it will keep them on the hope page.
    @app.route('/balanceRedirect', methods=['GET','POST'])
    def balanceRedirect():
        folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(folder_path)
        file = request.files['manifest-input-balance']
        filename = secure_filename(file.filename)
        if len(Manifest_Folder) == 0: 
            manifest_path = (os.path.join(app.root_path+'\ManifestFolder', filename))
            file.save(manifest_path)
            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.
                num_containers = sum(1 for containers in grid_data.values() for c in containers if c.name not in ['NAN', 'UNUSED'])
                Manifest_Folder = os.listdir(folder_path)
                file_path_log = 'log.txt'

                with open(file_path_log, 'a') as files:
                    files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + filename + ' manifest is opened for unloading/loading, there are ' + str(num_containers) + ' on the ship \n')
                    os.unlink(file_path_log)

            except Exception as e:
                print(f"ERRORRRRRR: {e}", "error")
                session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            session['manifest_file'] = filename
            tree = Tree(ignore)
            moves = tree.AStar()
            session['Solution'] = []
            for move in moves:
                print(move[0])
                session['Solution'].append(move[0])
            session['solution_data'] = session['Solution'][0]
            return redirect(url_for('auth.balance'))

            session['grid_data'] = { #I think that in order to allow the name to be displayed I want to store the name of the file somewher in here but I need to understand how Andrea sent this data to tasks_base
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            session['manifest_file'] = filename
            tree = Tree(ignore)
            moves = tree.AStar()
            session['Solution'] = []
            for move in moves:
                print(move[0])
                session['Solution'].append(move[0])
            session['solution_data'] = session['Solution'][0]
            return redirect(url_for('auth.balance'))
        else:
            if (Manifest_Folder[0] == 'instructions.txt'):
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[1]))
            else:
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[0]))
            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.

            except Exception as e:
                flash(f"ERRORRRRRR: {e}", "error")
                return redirect(url_for('home'))

            session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            session['manifest_file'] = filename
            tree = Tree(ignore)
            moves = tree.AStar()
            session['Solution'] = []
            for move in moves:
                print(move[0])
                session['Solution'].append(move[0])
            session['solution_data'] = session['Solution'][0]
            return redirect(url_for('auth.balance'))
    
    @app.route('/unload_loadRedirect', methods=['POST'])
    def unload_loadRedirect():
        #print(request.files)
        folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(folder_path)
        file = request.files['manifest-input-unload-load']
        filename = secure_filename(file.filename)
        if len(Manifest_Folder) == 0: 
            manifest_path = (os.path.join(app.root_path+'\ManifestFolder', filename))
            file.save(manifest_path)
            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.
                num_containers = sum(1 for containers in grid_data.values() for c in containers if c.name not in ['NAN', 'UNUSED'])
                Manifest_Folder = os.listdir(folder_path)
                file_path_log = 'log.txt'

                with open(file_path_log, 'a') as files:
                    files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + filename + ' manifest is opened for unloading/loading, there are ' + str(num_containers) + ' on the ship \n')
                    os.unlink(file_path_log)

            except Exception as e:
                print(f"ERRORRRRRR: {e}", "error")
                session['grid_data'] = { #I think that in order to allow the name to be displayed I want to store the name of the file somewher in here but I need to understand how Andrea sent this data to tasks_base
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
                session['manifest_file'] = filename
                return redirect(url_for('auth.unload_load'))
            
            session['grid_data'] = { #I think that in order to allow the name to be displayed I want to store the name of the file somewher in here but I need to understand how Andrea sent this data to tasks_base
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            session['manifest_file'] = filename
            return redirect(url_for('auth.unload_load'))
        else:
            if (Manifest_Folder[0] == 'instructions.txt'):
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[1]))
            else:
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[0]))
            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.

            except Exception as e:
                flash(f"ERRORRRRRR: {e}", "error")
                return redirect(url_for('home'))
                
            session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            session['manifest_file'] = filename
            return redirect(url_for('auth.unload_load'))

    @app.route('/unloadLoadRequest', methods=['POST']) #This isn't being seen for some reason
    def unloadLoadRequest():
        file_path = 'Website/ManifestFolder/instructions.txt'
        data = request.json
        with open(file_path, 'a') as files:
            files.write(f"Action: {data.get('action')}, Name: {data.get('name')}, Weight: {data.get('weight')}\n")
        return jsonify({"message": "Success!"})


    @app.route('/completeCycle', methods=['POST'])
    def completeCycle():
        manifest_folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(manifest_folder_path)
        file_path = 'log.txt'
        solution_folder_path = "Website\Solution"
        Solution_Folder = os.listdir(solution_folder_path)
        outbound_Folder = os.listdir("Website\outbound")
        if(outbound_Folder[0]):
            outbound_name = outbound_Folder[0]
            outbound_file_path = os.path.join(app.root_path + '\outbound', outbound_name)
            return redirect(url_for('auth.placeholder'))

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' Cycle Complete.\n')
        for file in Manifest_Folder:
            manifest_file_path = os.path.join(manifest_folder_path, file)
            os.unlink(manifest_file_path)
        for file in Solution_Folder:
            solution_file_path = os.path.join(solution_folder_path, file)
            os.unlink(solution_file_path)
        session['solution_data'] = []
        print(session['solution_data'])
        session['Solution'] = []
        return redirect(url_for('auth.home'))
    
    @app.route('/findSolution', methods=['POST'])
    def findSolution():
        folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(folder_path)
        if(len(Manifest_Folder) > 1):
            if (Manifest_Folder[0] == 'instructions.txt'):
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[1]))
            if (Manifest_Folder[1] == 'instructions.txt'):
                manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[0]))
        else:
            return ('', 204)
        file_path = 'Website/ManifestFolder/instructions.txt'
        load, unload = iparse(file_path)
        for i in range(len(load)):
            load[i] = A_Container(0, load[i])
        for i in range(len(unload)):
            unload[i] = A_Container(0, unload[i])
        igrid,_ = parse(manifest_path)
        tree = LTree(manifest_path, unload, load, igrid)
        moves = tree.aStar()
        session['Solution'] = []
        for move in moves:
            print(move)
            session['Solution'].append(move['description'])
        session['solution_data'] = session['Solution'][0]
        
        return redirect(url_for('auth.unload_load'))

    @app.route('/nextInstruction', methods=['POST'])
    def nextInstruction():
        for i in range(len(session['Solution'])):
            if (session['solution_data'] == session['Solution'][i]):
                print(i)
                print(len(session['Solution'])-1)
                if(i != len(session['Solution'])-1):
                    session['solution_data'] = session['Solution'][i+1]
                    return redirect(url_for('auth.unload_load'))
                if( i == len(session['Solution'])-1):
                    session['solution_data'] = "Cycle Complete. Please click the cycle complete button."
        return redirect(url_for('auth.unload_load'))
    
    @app.route('/nextBalanceInstruction', methods=['POST'])
    def nextBalanceInstruction():
        for i in range(len(session['Solution'])):
            if (session['solution_data'] == session['Solution'][i]):
                print(i)
                print(len(session['Solution'])-1)
                if(i != len(session['Solution'])-1):
                    session['solution_data'] = session['Solution'][i+1]
                    return redirect(url_for('auth.balance'))
                if( i == len(session['Solution'])-1):
                    session['solution_data'] = "Cycle Complete. Please click the cycle complete button."
        return redirect(url_for('auth.balance'))


    return app


def solution_parse(file_path):
    solutions_line = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip(): 
                    solutions_line.append(line.strip())
    except FileNotFoundError:
        print("Error: Solution file not found.")
    except Exception as e:
        print(f"Error while parsing solutions: {e}")

    return solutions_line
