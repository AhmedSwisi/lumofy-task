import  { useState } from 'react';
import { useCourses } from '../api/courses';
import { 
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious, 
} from './ui/pagination'; 
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardFooter,
  } from "./ui/card"; 

  const Courses = () => {
    const [page, setPage] = useState(1);
    const { data, isLoading, isError, error } = useCourses(page);
  
    if (isLoading) {
      return <div>Loading...</div>;
    }
  
    if (isError) {
      return <div>Error: {error instanceof Error ? error.message : 'Error fetching courses'}</div>;
    }
  
    const totalPages = Math.ceil((data?.count || 0) / 10); // Assuming 10 items per page
    const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);  // Create array for page numbers
  
    // Function to handle page change
    const handlePageChange = (newPage: number) => {
      setPage(newPage);
    };
  
    return (
      <div>
        <h1 className="text-xl font-bold">Courses</h1>
  
        {/* Courses grid layout */}
        <div className="grid grid-cols-[repeat(auto-fit,_minmax(300px,_1fr))] gap-4">
          {data?.results.map((course) => (
            <Card key={course.id} className="mb-4">
              <CardHeader>
                <CardTitle>{course.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p>{course.description}</p>
                <p><strong>Teachers:</strong> {course.teachers.join(', ')}</p>
                <p><strong>Lessons:</strong> {course.lessons.length > 0 ? course.lessons.join(', ') : 'No lessons available'}</p>
              </CardContent>
              <CardFooter>
                {/* Add any footer details */}
              </CardFooter>
            </Card>
          ))}
        </div>
  
        {/* Pagination */}
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
              size={"sm"}
                href="#"
                onClick={() => handlePageChange(page - 1)}
                className="pagination-link"
              >
                Previous
              </PaginationPrevious>
            </PaginationItem>
  
            {pageNumbers.map((pageNumber) => (
              <PaginationItem key={pageNumber}>
                <PaginationLink
                size={"sm"}
                  href="#"
                  isActive={pageNumber === page}
                  onClick={() => handlePageChange(pageNumber)}
                  className="pagination-link"
                >
                  {pageNumber}
                </PaginationLink>
              </PaginationItem>
            ))}
  
            <PaginationItem>
              <PaginationNext
              size={"sm"}
                href="#"
                onClick={() => handlePageChange(page + 1)}
                className="pagination-link"
              >
                Next
              </PaginationNext>
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    );
  };
  
  export default Courses;