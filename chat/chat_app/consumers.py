import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
class QuizConsumer(AsyncWebsocketConsumer):
    connected_users = 0  # Class variable to track connected users
    answer_received = 0

    async def connect(self):
        # Check if the room is full
        self.room_name = "quiz_room"  # Customize this based on your requirements
        cache.set(f"{self.room_name}_answers", 0)  # Initialize answer count for the room
        await self.channel_layer.group_add(
        self.room_name,
        self.channel_name)
        cache.set(f"{self.room_name}_answers", 0) 

        if QuizConsumer.connected_users >= 2:
            print('ABORT!!!!!')
            await self.close()  # Close the connection if the room is full
            # return 

        QuizConsumer.connected_users += 1  # Increment connected users
        print('connected : ',self.connected_users)
        self.current_question_index = 0
        self.questions = [
            {'text': 'What is A?', 'options': ['apple', 'ball', 'cat', 'dog'], 'correct_option': 'apple'},
            {'text': 'What is B?', 'options': ['X', 'Y', 'Z'], 'correct_option': 'Y'},
            {'text': 'What is C?', 'options': ['1', '2', '3'], 'correct_option': '1'},
            {'text': 'What is D?', 'options': ['red', 'blue', 'green'], 'correct_option': 'red'},
            {'text': 'What is E?', 'options': ['car', 'bus', 'train'], 'correct_option': 'car'}
        ]
        await self.accept()

    async def disconnect(self, close_code):
        QuizConsumer.connected_users -= 1  # Decrement connected users

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'start_quiz':
            print('quiz_status : ', 'start')
            await self.send_question(self.questions[self.current_question_index])
        elif data['type'] == 'answer':
            answers = data['answer']
            print('answer : ', answers)
            await self.handle_answer(answers)

    async def send_question(self, question):
        await self.channel_layer.group_send(
        self.room_name,
        {
            'type': 'broadcast_question',
            'question': question
        })

    async def handle_answer(self, answer):    
       answer_count = cache.get(f"{self.room_name}_answers", 0) 
       answer_count += 1
       await self.check_answer(answer)
       print(answer_count)
       cache.set(f"{self.room_name}_answers", answer_count)
       if answer_count == 2 :
            cache.set(f"{self.room_name}_answers", 0)  # Reset answer count for the room
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                await self.send_question(self.questions[self.current_question_index])
    
    async def broadcast_question(self, event):
        question = event['question']
        await self.send(json.dumps({
            'type': 'question',
            'question': question
            }))
        
    
    async def check_answer(self,answer):
        if answer == self.questions[self.current_question_index].get('correct_option'):
            print('status : ','correct')
            await self.send(json.dumps({
                'type':'check',
                'status':'correct'
            }))
            return
        else:
            print('status : ','wrong')
            await self.send(json.dumps({
                'type':'check',
                'status':'wrong',
                'correct_answer': self.questions[self.current_question_index].get('correct_option')
            }))
            return