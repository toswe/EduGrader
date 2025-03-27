export interface ICourse {
  id: number;
  name: string;
}

export interface IQuestion {
  id: number;
  question: string;
  answer: string;
  course: number;
}

export interface ITest {
  id: number;
  name: string;
  course: number;
  questions: IQuestion[] | number[];
}
