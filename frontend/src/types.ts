export interface IJwtPayload {
  user_id: string;
  username: string;
  type: "STUDENT" | "PROFESSOR";
}

export interface IUser {
  isAuthenticated: boolean;
  id: number;
  username: string;
  type: "STUDENT" | "PROFESSOR" | null;
}

export interface ICourse {
  id: number;
  name: string;
}

export interface IQuestion {
  id: number;
  question: string;
  answer: string;
  course?: number;
}

export interface ITest {
  id: number;
  name: string;
  course: number;
  questions: number[];
  configuration: object;
}

export interface ITestQuestions extends Omit<ITest, "questions"> {
  questions: IQuestion[];
}

export interface IAnswerGrade {
  id?: number;
  prompt: string;
  llm_response: any;
  score: number;
  student_answer: number; // ID of the student's answer
}

export interface IStudentAnswer {
  id?: number;
  studentTest?: number;
  question: number;
  questionText: string;
  answer: string;
  grades?: IAnswerGrade[];
}

export interface IStudentTest extends Object {
  id?: number;
  student?: number;
  test: number;
  answers: IStudentAnswer[];
}
