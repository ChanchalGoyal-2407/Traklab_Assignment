# Traklab_Assignment
from flask import Flask,make_response,request,jsonify
from flask_mongoengine import MongoEngine
import logging.config
# Logger().setup_logging()
logger = logging.getLogger(__name__)


app= Flask(__name__)
database_name="API"
DB_URI=""     # connection to MongoDB Atlas Cluster and password

db=MongoEngine()
db.init_app(app)

class Employee(db.Document):
    
    employee_id=db.IntField()
    name=db.StringField()
    department=db.StringField()
    
    def to_json(self):
        
        return {
            "employee_id":self.employee_id,
            "name":self.name,
            "department":self.department
            }
    
        
    @app.route('/api/db_populate',methods=['POST'])
    def db_populate():
        
        employee1 = Employee(employee_id=1,
                           name="chanchal",
                           department="cse")
        employee2 = Employee(employee_id=2,
                           name="Sweety",
                           department="ece")
        employee1.save()
        employee2.save()
        return make_response('',201)
    
    
    @app.route('/api/employees',methods=['GET','POST'])
    def api_employees():
        try:
            if request.method== 'GET':
                employees=[]
                for employee in Employee.objects:
                    employees.append(employee)
                return make_response(jsonify(employees),200)
            
            elif  request.method== 'POST':
                content = request.json
                
                employee = Employee(employee_id=content['employee_id'],
                                    name=content['name'],
                                    department=content['department'])
                employee.save()
                return make_response("",201)
        except Exception as e:
            logger.error("Error occured in Employee POST/GET : {}".format(str(e)))
   
    
    @app.route('/api/employees/<employee_id>',methods=['GET','POST','DELETE'])
    def api_each_employee(employee_id):
        if request.method == "GET":
            employee_obj = Employee.objects(employee_id=employee_id).first()
            if  employee_obj:
                return make_response(jsonify(employee_obj.to_json()),200)
            else:
                return make_response('',404)
            
        elif request.method == 'PUT':
            content = request.json
            employee_obj=Employee.objects(employee_id=employee_id).first()
            employee_obj.update(department=content['department'],name=content['name'])
            return make_response('',204)
        
        elif request.method=="DELETE":
            employee_obj=Employee.objects(employee_id=employee_id).first()
            employee_obj.delete()
            return make_response('',204)            
            
            
        
if __name__=='__main__':
    app.run(debug=True)


