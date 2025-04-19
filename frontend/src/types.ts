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
}

export interface ITestQuestions extends Omit<ITest, "questions"> {
  questions: IQuestion[];
}

export interface IStudentTest {
  id?: number;
  student?: number;
  test: number;
  answers: IQuestion[];
}
