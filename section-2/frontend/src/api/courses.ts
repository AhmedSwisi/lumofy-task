import api from "./router";
import { useQuery } from "react-query";

interface Course {
    id:number,
    title:string,
    description:string
    teachers:string[],
    lessons:string[]
}

interface PaginatedResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: Course[];
  }

export const fetchCourses = async (page:number): Promise<PaginatedResponse> => {
    const response = await api.get<PaginatedResponse>(`/courses/?page=${page}`);
    return response.data;
  };

  export const useCourses = (page: number) => {
    return useQuery(['courses', page], () => fetchCourses(page), {
      staleTime: 1000 * 60 * 5,
      cacheTime: 1000 * 60 * 10,
    });
  };