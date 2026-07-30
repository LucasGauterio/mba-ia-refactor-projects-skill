const { dbQuery } = require('../config/database');

class Course {
    static async findById(id) {
        return dbQuery.get("SELECT * FROM courses WHERE id = ?", [id]);
    }

    static async findActiveById(id) {
        return dbQuery.get("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    }

    static async getFinancialReport() {
        // Optimized JOIN query preventing N+1 queries.
        const rows = await dbQuery.all(`
            SELECT 
                c.id AS course_id,
                c.title AS course_title,
                u.name AS student_name,
                p.amount AS payment_amount,
                p.status AS payment_status
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            LEFT JOIN users u ON e.user_id = u.id
            LEFT JOIN payments p ON e.id = p.enrollment_id
            ORDER BY c.id ASC
        `);

        const reportMap = {};
        for (const row of rows) {
            if (!reportMap[row.course_id]) {
                reportMap[row.course_id] = {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                };
            }
            
            // Checking if there is an actual student enrolled (handling LEFT JOIN nulls)
            if (row.student_name !== null && row.student_name !== undefined) {
                const paidAmount = row.payment_amount !== null ? row.payment_amount : 0;
                
                if (row.payment_status === 'PAID') {
                    reportMap[row.course_id].revenue += row.payment_amount;
                }
                
                reportMap[row.course_id].students.push({
                    student: row.student_name || 'Unknown',
                    paid: paidAmount
                });
            }
        }

        return Object.values(reportMap);
    }
}

module.exports = Course;
