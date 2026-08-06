const { db } = require('../config/database');

class ReportModel {
    static getFinancialReport() {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT 
                    c.id AS course_id,
                    c.title AS course_title,
                    u.name AS student_name,
                    p.amount AS payment_amount,
                    p.status AS payment_status,
                    e.id AS enrollment_id
                FROM courses c
                LEFT JOIN enrollments e ON c.id = e.course_id
                LEFT JOIN users u ON e.user_id = u.id
                LEFT JOIN payments p ON e.id = p.enrollment_id
            `;
            db.all(sql, [], (err, rows) => {
                if (err) return reject(err);
                
                const reportMap = new Map();
                
                rows.forEach(row => {
                    if (!reportMap.has(row.course_id)) {
                        reportMap.set(row.course_id, {
                            course: row.course_title,
                            revenue: 0,
                            students: []
                        });
                    }
                    
                    const courseData = reportMap.get(row.course_id);
                    
                    if (row.enrollment_id !== null) {
                        const amount = row.payment_amount !== null ? row.payment_amount : 0;
                        if (row.payment_status === 'PAID') {
                            courseData.revenue += amount;
                        }
                        
                        courseData.students.push({
                            student: row.student_name || 'Unknown',
                            paid: amount
                        });
                    }
                });
                
                resolve(Array.from(reportMap.values()));
            });
        });
    }
}

module.exports = ReportModel;
