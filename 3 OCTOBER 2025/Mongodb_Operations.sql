//INSERT MANY 
db.students.insertMany([
  { student_id: 2, name: "Priya", age:22, city:"Delhi", course:"ML", marks:90},
  { student_id: 3, name: "Arjun", age:20, city:"Bengaluru", course:"Data Science", marks:78},
  { student_id: 4, name: "Neha", age:23, city:"Hyderabad", course:"AI", marks:88},
  { student_id: 5, name: "Vikram", age:21, city:"Chennai", course:"ML", marks:95}
])
  
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfa867d820ec06268084b3'),
    '1': ObjectId('68dfa867d820ec06268084b4'),
    '2': ObjectId('68dfa867d820ec06268084b5'),
    '3': ObjectId('68dfa867d820ec06268084b6')
  }
}
//FIND VALUES SAME AS SELECT
db.students.find()


{
  _id: ObjectId('68dfa867d820ec06268084b3'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa867d820ec06268084b4'),
  student_id: 3,
  name: 'Arjun',
  age: 20,
  city: 'Bengaluru',
  course: 'Data Science',
  marks: 78
}
{
  _id: ObjectId('68dfa867d820ec06268084b5'),
  student_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}
{
  _id: ObjectId('68dfa867d820ec06268084b6'),
  student_id: 5,
  name: 'Vikram',
  age: 21,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}

//FINDING ONE VALUE
db.students.findOne({name: "Neha"})

{
  _id: ObjectId('68dfa867d820ec06268084b5'),
  student_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}

db.students.find({},{ name: 1, course: 1,_id:0})

output
{
  name: 'Priya',
  course: 'ML'
}
{
  name: 'Arjun',
  course: 'Data Science'
}
{
  name: 'Neha',
  course: 'AI'
}
{
  name: 'Vikram',
  course: 'ML'
}
//UPDATING ONE VALUE

db.students.updateOne(
  { name: "Neha"},
  {$set: {marks:92,course: "Advanced AI"}}
)


{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}

//DELETE
db.students.deleteOne({name:"Arjun"})

output
{
  acknowledged: true,
  deletedCount: 1
}


db.students.deleteMany({marks:{$lt: 80 }})

output
{
  acknowledged: true,
  deletedCount: 0
}
